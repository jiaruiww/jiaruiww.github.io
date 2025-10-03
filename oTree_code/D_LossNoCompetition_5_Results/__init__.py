from otree.api import *
import sys
import os
import time

# Try to import global functions (safe fallback)
try:
    from global_functions import get_progress, update_progress, initialize_progress
except ImportError:
    # Keep backup implementation in case import fails
    def initialize_progress(player):
        if 'total_progress_units' not in player.participant.vars:
            player.participant.vars['total_progress_units'] = C.TOTAL_PROGRESS_UNITS
            player.participant.vars['current_progress'] = 0
            player.participant.vars['pages_viewed'] = set()


    def get_progress(player, page_name=None):
        initialize_progress(player)
        current_progress = player.participant.vars['current_progress']
        total_units = player.participant.vars['total_progress_units']
        progress_percent = int((current_progress / total_units) * 100)
        return {'progress_percent': progress_percent}


    def update_progress(player, page_name):
        initialize_progress(player)
        pages_viewed = player.participant.vars.get('pages_viewed', set())
        if page_name not in pages_viewed:
            pages_viewed.add(page_name)
            player.participant.vars['pages_viewed'] = pages_viewed
            player.participant.vars['current_progress'] += 1
        return get_progress(player, page_name)


class C(BaseConstants):
    NAME_IN_URL = 'A4_LC_5_Results'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    PROLIFIC_COMPLETION_CODE = 'CD1QQQ6K'

    QUIZ_THRESHOLD_SCORE = 6

    APP3_PAGES = 6  # A4_LC_3_Survey page count
    APP4_PAGES = 4  # A4_LC_4_Decision_P page count
    APP5_PAGES = 7  # Current app page count
    TOTAL_PROGRESS_UNITS = APP3_PAGES + APP4_PAGES + APP5_PAGES  # = 22


# Add helper function to ensure prolific_id can always be obtained
def ensure_prolific_id(player):
    """Ensure player's prolific_id field has a value, try multiple sources"""

    # If prolific_id already has a value, return directly
    if player.prolific_id and player.prolific_id.strip():
        return player.prolific_id

    # Try to get from participant.vars
    if 'prolific_id' in player.participant.vars and player.participant.vars['prolific_id']:
        player.prolific_id = player.participant.vars['prolific_id']
        return player.prolific_id

    # Try to get from participant.label
    if player.participant.label and player.participant.label.strip():
        player.prolific_id = player.participant.label
        # Also save to participant.vars for later use
        player.participant.vars['prolific_id'] = player.participant.label
        return player.prolific_id

    # If all above fail, return empty string
    return ""


class Subsession(BaseSubsession):
    def creating_session(self):
        # Initialize progress tracking
        for p in self.get_players():
            initialize_progress(p)

            # Enhanced version of prolific_id retrieval, using helper function
            p.prolific_id = ensure_prolific_id(p)

            # Progress initialization:
            if p.participant.vars.get('app4_completed', False):
                p.participant.vars['current_progress'] = C.APP3_PAGES + C.APP4_PAGES  # = 11


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # Add prolific_id field
    prolific_id = models.StringField(default="", blank=True)

    # Add time tracking fields
    attention_check_time = models.FloatField(initial=0)  # New field for attention check
    confidence_time = models.FloatField(initial=0)
    relative_performance_time = models.FloatField(initial=0)
    enjoy_competing_time = models.FloatField(initial=0)
    enjoy_competition_two_time = models.FloatField(initial=0)

    # New time tracking fields for political survey pages
    understanding_time = models.FloatField(initial=0)
    comments_time = models.FloatField(initial=0)
    quiz_results_time = models.FloatField(initial=0)
    debriefing_time = models.FloatField(initial=0)
    completion_time = models.FloatField(initial=0)

    # Fix attention check field - add blank=True to allow empty
    attention_check_response = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label="Please select your response on the scale from 0 to 10",
        blank=True  # Allow empty, so user can choose not to select any option
    )

    # IQ Quiz win belief
    won_iq_quiz = models.BooleanField(
        choices=[
            [True, 'Yes'],
            [False, 'No']
        ],
        label="Do you think you won the IQ Quiz Competition? (If your answer is correct, you will receive an extra $0.2 bonus.)"
    )

    # Relative performance perception
    relative_performance = models.IntegerField(
        choices=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        label="Based on your experience in the IQ Quiz competition, how well do you think you performed compared to all other participants in this study?"
    )

    # Update just this part of the Player class
    enjoy_competing = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label='"Competition brings the best out of me."',
        widget=widgets.RadioSelect
    )

    # Update just this part of the Player class
    prefer_competitive_environment = models.IntegerField(
        choices=[1, 2, 3, 4, 5, 6, 7],
        label='"I enjoy competing against others."',
        widget=widgets.RadioSelect
    )


    # Understanding check
    understood_rules = models.StringField(
        choices=[
            ('fully', 'Fully understood'),
            ('almost_fully', 'Almost fully understood'),
            ('partly', 'Partly understood'),
            ('not', 'Not understood')
        ],
        label="Did you understand the rules of this study?",
        widget=widgets.RadioSelect
    )

    # Comments field
    comments = models.LongStringField(
        label="Do you have any comments or feedback about this study?",
        blank=True
    )

    app5_completed = models.BooleanField(default=False, doc="Completed A1_GT_5_Results")

    # Demographics fields
    birth_year = models.IntegerField(min=1920, max=2010, label="Birth year")
    gender = models.StringField(
        choices=[
            ['male', 'Male'],
            ['female', 'Female'],
            ['other', 'Other']
        ],
        label="Gender"
    )
    race_ethnicity = models.StringField(
        choices=[
            ['white', 'White'],
            ['african_american', 'African-American'],
            ['hispanic', 'Hispanic'],
            ['american_indian', 'American Indian or Alaska Native'],
            ['asian', 'Asian'],
            ['other', 'Other']
        ],
        label="Race or ethnicity"
    )
    education = models.StringField(
        choices=[
            ['no_high_school', 'No high school graduation'],
            ['high_school', 'High school graduate'],
            ['bachelors', "Bachelor's degree"],
            ['graduate', 'Graduate or professional degree']
        ],
        label="Educational attainment"
    )
    income = models.StringField(
        choices=[
            ['below_10000', 'Below 10,000'],
            ['10000_14999', '10,000–14,999'],
            ['15000_24999', '15,000–24,999'],
            ['25000_34999', '25,000–34,999'],
            ['35000_49999', '35,000–49,999'],
            ['50000_74999', '50,000–74,999'],
            ['75000_99999', '75,000–99,999'],
            ['100000_149999', '100,000–149,999'],
            ['150000_199999', '150,000–199,999'],
            ['200000_more', '200,000 or more']
        ],
        label="Annual household income before taxes"
    )
    employment = models.StringField(
        choices=[
            ['yes', 'Yes'],
            ['no', 'No']
        ],
        label="Employed full-time"
    )
    economic_spectrum = models.StringField(
        choices=[
            ['extreme_left', 'Extreme Left'],
            ['leaning_left', 'Leaning Left'],
            ['center', 'Center'],
            ['leaning_right', 'Leaning Right'],
            ['extreme_right', 'Extreme Right']
        ],
        label="Economic policy spectrum"
    )

    # Add time tracking field for demographics page
    demographics_time = models.FloatField(initial=0)


class AttentionCheckPage(Page):
    form_model = 'player'
    form_fields = ['attention_check_response']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        # Fix: Ensure progress continues from where 4th app ended
        if (player.participant.vars.get('app4_completed', False) and
                'AttentionCheckPage_App5' not in player.participant.vars.get('pages_viewed', set())):
            player.participant.vars['current_progress'] = C.APP3_PAGES + C.APP4_PAGES  # = 11

        return update_progress(player, 'AttentionCheckPage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player


class ConfidencePage(Page):
    form_model = 'player'
    form_fields = ['won_iq_quiz']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'ConfidencePage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.confidence_time = time.time() - start_time


class RelativePerformancePage(Page):
    form_model = 'player'
    form_fields = ['relative_performance']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'RelativePerformancePage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.relative_performance_time = time.time() - start_time


class EnjoyCompetingOnePage(Page):
    form_model = 'player'
    form_fields = ['enjoy_competing']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'EnjoyCompetingOnePage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.enjoy_competing_time = time.time() - start_time


class EnjoyCompetitionTwoPage(Page):
    form_model = 'player'
    form_fields = ['prefer_competitive_environment']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'EnjoyCompetitionTwoPage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.enjoy_competition_two_time = time.time() - start_time



class UnderstandingPage(Page):
    form_model = 'player'
    form_fields = ['understood_rules']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'UnderstandingPage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.understanding_time = time.time() - start_time


class DemographicsPage(Page):
    form_model = 'player'
    form_fields = ['birth_year', 'gender', 'race_ethnicity', 'education', 'income', 'employment', 'economic_spectrum']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        return update_progress(player, 'DemographicsPage_App5')

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.demographics_time = time.time() - start_time


class CommentsPage(Page):
    form_model = 'player'
    form_fields = ['comments']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        # No progress bar for this page - just return an empty dict
        return {}

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.comments_time = time.time() - start_time

class QuizResultsPage(Page):
    """Display the final results from the IQ quiz competition"""

    @staticmethod
    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        # Get the competition results from participant.vars
        # These would have been stored during the quiz app's Results page
        competition_results = player.participant.vars.get('competition_results', {})

        # Extract the values needed for the template
        total_questions_attempted = competition_results.get('total_questions_attempted', 0)
        player_score = competition_results.get('player_score', 0)
        opponent_score = competition_results.get('opponent_score', 0)
        result_message = competition_results.get('result_message', "")

        vars_dict = {
            'total_questions_attempted': total_questions_attempted,
            'player_score': player_score,
            'opponent_score': opponent_score,
            'result_message': result_message
        }

        # No progress bar for this page
        return vars_dict

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.quiz_results_time = time.time() - start_time


class DebriefingPage(Page):
    """Debriefing page to explain the full purpose of the study to participants"""

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        # No progress bar for this page - just return an empty dict
        return {}

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.debriefing_time = time.time() - start_time


class CompletionPage(Page):
    """Final page for automatic redirect to Prolific"""

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure prolific_id field always has a value
        player.prolific_id = ensure_prolific_id(player)

        # Get prolific completion code from the constant
        prolific_completion_code = C.PROLIFIC_COMPLETION_CODE

        # Also set completion flag here (when page loads)
        player.app5_completed = True

        # Get Prolific completion URL (usually set in SESSION_CONFIGS in settings.py)
        prolific_completion_url = player.session.config.get(
            'prolific_completion_url',
            f'https://app.prolific.com/submissions/complete?cc={prolific_completion_code}'
        )

        vars_dict = {
            'prolific_completion_url': prolific_completion_url,
            'prolific_completion_code': prolific_completion_code  # Pass to template
        }

        # No progress bar for this page
        return vars_dict

    def before_next_page(player, timeout_happened):
        # Calculate page time spent
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.completion_time = time.time() - start_time

        # Ensure app5 completion flag is set again
        player.app5_completed = True

        # Also save a copy in participant.vars
        player.participant.vars['app5_completed'] = True


page_sequence = [
    AttentionCheckPage,  # New attention check page added first
    ConfidencePage,
    RelativePerformancePage,
    EnjoyCompetingOnePage,
    EnjoyCompetitionTwoPage,
    UnderstandingPage,
    DemographicsPage,
    CommentsPage,
    QuizResultsPage,
    DebriefingPage,
    CompletionPage
]