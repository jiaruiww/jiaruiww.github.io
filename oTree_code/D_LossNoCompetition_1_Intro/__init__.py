from otree.api import *
from time import time
from os import environ
import requests  # Uncommented for reCAPTCHA verification

doc = """
Combined app integrating A_GT_1_OpeningPage and A_GT_2_Instructions.
This combines the welcome, consent and Prolific ID collection screens with the 
instructions and practice question sections into a single cohesive app.
"""


# ===== Time Tracking Utility (Float Version) =====
def track(cls):
    """Decorator for tracking time spent on pages with float precision."""
    orig_get = cls.get
    orig_post = cls.post

    def tracking_get(page):
        now = time()  # Keep original float value
        page.participant.vars['_tracking_get_timestamp'] = now
        if '_tracking_first_timestamp' not in page.participant.vars:
            page.participant.vars['_tracking_first_timestamp'] = now
        if '_tracking_post_timestamp' in page.participant.vars:
            del page.participant.vars['_tracking_post_timestamp']
        return orig_get(page)

    def tracking_post(page):
        page.participant.vars['_tracking_post_timestamp'] = time()  # Keep float value
        return orig_post(page)

    cls.get = tracking_get
    cls.post = tracking_post
    return cls


def last(participant):
    """Get the time spent on the last page in seconds (float precision)."""
    return participant.vars['_tracking_post_timestamp'] - participant.vars['_tracking_get_timestamp']


def total(participant):
    """Get the total time spent across all pages in seconds (float precision)."""
    return participant.vars['_tracking_post_timestamp'] - participant.vars['_tracking_first_timestamp']



# ===== reCAPTCHA Verification Function =====
from os import environ


def verify_recaptcha(recaptcha_response):
    """Verify reCAPTCHA response with Google's API."""
    # Get secret key from environment variable, or use fallback value
    secret_key = "6LfpUtoqAAAAALflSsdI10lUPryBmNBtuIvFHe88"  # Replace with your actual secret key
    verification_url = "https://www.google.com/recaptcha/api/siteverify"
    data = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    try:
        response = requests.post(verification_url, data=data, timeout=5)
        result = response.json()
        return result.get('success', False)
    except Exception as e:
        print(f"reCAPTCHA verification failed. Please try again.: {e}")
        return False


# ===== Constants & Models =====
class C(BaseConstants):
    NAME_IN_URL = 'A4_LC_1_Intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    # Define payment and threshold variables
    THRESHOLD_SCORE = 6
    PENALTY_AMOUNT = 4
    BASE_PAYMENT = 6

    # Intro comprehension question choices
    INTRO_COMP_CHOICES = [
        ("A", "No"),
        ("B", "Yes"),
        ("C", "Not enough information"),
    ]

    # Practice question choices
    PRACTICE_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]


class Subsession(BaseSubsession):
    def creating_session(self):
        """Initialize session-level tracking to ensure we have data even for early exits"""
        for player in self.get_players():
            # Ensure we capture the participant's ID from Prolific if available
            if player.participant.label:
                player.prolific_id = player.participant.label

            # Initialize practice question fields
            player.practice_attempts = 0
            player.practice_attempt_history = ""
            player.practice_answer = ""  # Initialize practice_answer to empty string

            # Initialize comprehension question attempt tracking
            player.intro_comp_attempts = 0
            player.intro_comp_attempt_history = ""


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # User identification
    prolific_id = models.StringField(default=str(" "), label=" ")

    # reCAPTCHA verification field - Updated to StringField
    captcha_verified = models.StringField(initial="false")

    # Added field to store the actual reCAPTCHA response token
    recaptcha_response = models.StringField(initial="")

    # Consent tracking
    consent_given = models.BooleanField(default=False)

    # Time tracking for each page from App 1
    time_welcome_page = models.FloatField(blank=True, null=True)
    time_first_page = models.FloatField(blank=True, null=True)
    time_prolific_id_page = models.FloatField(blank=True, null=True)

    # Cumulative time tracking from App 1
    time_until_first = models.FloatField(blank=True, null=True)

    # Intro comprehension question
    intro_comp_answer = models.StringField(
        label=f"In the 4-minute IQ Quiz, "
              f"Emily answers 10 questions (6 correct, 4 incorrect). "
              f"Does she <strong>lose ${C.PENALTY_AMOUNT}</strong> from the initial payment of ${C.BASE_PAYMENT}? <br> ",
        choices=C.INTRO_COMP_CHOICES,
        widget=widgets.RadioSelect
    )
    intro_comp_correct = models.BooleanField()

    # NEW: Fields to track comprehension question attempts
    intro_comp_attempts = models.IntegerField(initial=0)  # Count of attempts
    intro_comp_attempt_history = models.StringField(initial="")  # Record of all attempts (e.g., "A,B,C")

    # Practice question fields
    practice_answer = models.StringField(
        label="Which piece is the right complement?",
        choices=C.PRACTICE_CHOICES,
        widget=widgets.RadioSelect
    )
    practice_correct = models.BooleanField()  # To track if practice answer is correct

    # Fields to track practice attempts
    practice_attempts = models.IntegerField(initial=0)  # Count of attempts
    practice_attempt_history = models.StringField(initial="")  # Record of all attempts

    # Time tracking fields from App 2
    time_introduction = models.FloatField(initial=0.0)  # Float initial value
    time_practice = models.FloatField(initial=0.0)
    time_quiz_start = models.FloatField(initial=0.0)
    time_total = models.FloatField(initial=0.0)

    app1_completed = models.BooleanField(default=False, doc="Completed A1_1_Intro")


# ===== Pages =====
@track
class WelcomePage(Page):
    """Welcome Page from App 1"""

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_welcome_page = last(player.participant)


@track
class FirstPage(Page):
    """Consent form page from App 1"""
    form_model = 'player'
    form_fields = ['consent_given']

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_first_page = last(player.participant)
        player.time_until_first = total(player.participant)


@track
class ProlificID_Robot(Page):
    """Prolific ID collection with reCAPTCHA"""
    form_model = 'player'
    form_fields = ['prolific_id', 'captcha_verified', 'recaptcha_response']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'initial_prolific_id': player.prolific_id if player.prolific_id else player.participant.label,
            'captcha_failed': player.participant.vars.get('captcha_failed', False)
        }

    @staticmethod
    def error_message(player, values):
        # Check if Prolific ID is provided
        if not values.get('prolific_id'):
            return {
                'prolific_id': 'Please enter your Prolific ID.'
            }

        # Verify the reCAPTCHA response with Google's API
        recaptcha_token = values.get('recaptcha_response', '')
        if not recaptcha_token:
            player.participant.vars['captcha_failed'] = True
            return {
                'recaptcha_response': 'Please complete the reCAPTCHA verification.'
            }

        # Perform actual verification with Google's API
        recaptcha_verified = verify_recaptcha(recaptcha_token)
        if not recaptcha_verified:
            player.participant.vars['captcha_failed'] = True
            return {
                'recaptcha_response': 'reCAPTCHA verification failed. Please try again.'
            }

        # Clear failed flag if everything is valid
        player.participant.vars['captcha_failed'] = False

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.time_prolific_id_page = last(player.participant)

        # Store Prolific ID if provided
        if player.prolific_id:
            # Save Prolific ID to participant.vars for use across apps
            player.participant.vars['prolific_id'] = player.prolific_id


@track
class Introduction(Page):
    """Introduction Page with comprehension question from App 2"""
    form_model = 'player'
    form_fields = ['intro_comp_answer']

    @staticmethod
    def vars_for_template(player):
        return {
            'threshold_score': C.THRESHOLD_SCORE,
            'penalty_amount': C.PENALTY_AMOUNT,
            'base_payment': C.BASE_PAYMENT,
        }

    @staticmethod
    def error_message(player, values):
        answer = values.get('intro_comp_answer')
        if not answer:
            return {'intro_comp_answer': "Please select an answer."}

        if answer != "B":
            player.intro_comp_attempts += 1
            if player.intro_comp_attempt_history:
                player.intro_comp_attempt_history += f",{answer}"
            else:
                player.intro_comp_attempt_history = answer
            return {'intro_comp_answer': ""}

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Always increment counter, regardless of whether it's the first correct answer
        if player.intro_comp_answer == "B":
            player.intro_comp_attempts += 1  # Always increment counter

            # Record correct answer
            if player.intro_comp_attempt_history:
                player.intro_comp_attempt_history += f",{player.intro_comp_answer}"
            else:
                player.intro_comp_attempt_history = player.intro_comp_answer

        player.intro_comp_correct = (player.intro_comp_answer == "B")
        player.time_introduction = last(player.participant)

    @staticmethod
    def js_vars(player):
        return {
            'custom_error_message': "Incorrect. Please review the instructions and try again."
        }


@track
class PracticeQuestion(Page):
    """Practice question with visual pattern from App 2"""
    form_model = 'player'
    form_fields = ['practice_answer']

    @staticmethod
    def vars_for_template(player):
        # Calculate the current attempt for display
        return {
            'current_attempt': player.practice_attempts + 1,
            'has_made_attempt': player.practice_attempts > 0
        }

    @staticmethod
    def error_message(player, values):
        answer = values.get('practice_answer')
        if not answer:
            return {'practice_answer': "Please select an answer."}

        if answer != "A":  # A is the correct answer
            player.practice_attempts += 1
            player.practice_attempt_history += f"{player.practice_attempts}:{answer},"
            return {'practice_answer': ""}

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Always increment counter, ensuring correct answers are also recorded
        if player.practice_answer == "A":
            player.practice_attempts += 1  # Always increment counter
            player.practice_attempt_history += f"{player.practice_attempts}:{player.practice_answer},"

        player.practice_correct = True
        player.time_practice = last(player.participant)


@track
class QuizAboutStart(Page):
    """Page shown before the actual IQ Quiz competition starts from App 2"""

    @staticmethod
    def vars_for_template(player):
        return {
            'threshold_score': C.THRESHOLD_SCORE,
            'penalty_amount': C.PENALTY_AMOUNT,
            'base_payment': C.BASE_PAYMENT,
        }

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Save time spent on this page
        player.time_quiz_start = last(player.participant)

        # Save total time spent across all pages
        # Since this is the last page in the sequence, we record total time here
        player.time_total = total(player.participant)

        # Set App1 completion flag
        player.participant.vars['app1_completed'] = True

        # Also save to Player model field
        player.app1_completed = True  # Need to add this field in Player class


# Page sequence
page_sequence = [
    WelcomePage,
    FirstPage,
    ProlificID_Robot,
    Introduction,
    PracticeQuestion,
    QuizAboutStart,
]