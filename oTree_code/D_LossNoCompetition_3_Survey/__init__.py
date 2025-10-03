from otree.api import *
import time
import sys
import os

# Safely import global progress functions
try:
    from global_functions import get_progress, update_progress, initialize_progress
except ImportError:
    # Fallback implementation in case import fails
    def initialize_progress(player):
        player.participant.vars.setdefault('total_progress_units', 20)
        player.participant.vars.setdefault('current_progress', 0)
        player.participant.vars.setdefault('pages_viewed', set())


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

doc = """
Survey for measuring enjoyment of a task and willingness to participate in future tasks for varying payments.
"""


class C(BaseConstants):
    NAME_IN_URL = 'A4_LC_3_Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    TOTAL_PROGRESS_UNITS = 6

    # Add these constants for the thresholds
    QUIZ_PENALTY_THRESHOLD = 6
    QUIZ_PENALTY_AMOUNT = 4
    BASE_PAYMENT = 6
    MIN_CORRECT_QUESTIONS = 5


class Subsession(BaseSubsession):
    def creating_session(self):
        grouped_players = []
        used_players = set()

        for p in self.get_players():
            if p.participant.id_in_session in used_players:
                continue

            partner_id = p.participant.vars.get('paired_partner_id')

            if partner_id:
                partner = next((pl for pl in self.get_players() if pl.participant.id_in_session == partner_id), None)
                if partner:
                    grouped_players.append([p, partner])
                    used_players.add(p.participant.id_in_session)
                    used_players.add(partner_id)

            # Only initialize progress, don't pass quiz data
            initialize_progress(p)
            p.participant.vars['app1_started'] = True

        self.set_group_matrix(grouped_players)


class Group(BaseGroup):
    pass


# Add unified data retrieval function
def get_quiz_data_for_player(player):
    """Dynamically retrieve quiz data, fetching latest data from participant.vars each time"""

    # Basic info
    player.prolific_id = player.participant.vars.get('prolific_id', '')

    # Get data from competition_results
    quiz_results = player.participant.vars.get('competition_results', {})

    if quiz_results:
        player.quiz_score = quiz_results.get('player_score', 0)
        player.quiz_questions_attempted = quiz_results.get('total_questions_attempted', 0)
        player.quiz_is_winner = quiz_results.get('is_winner', False)
        player.quiz_total_time = quiz_results.get('total_time_spent', 0)
        player.total_questions_attempted_with_skipped = quiz_results.get('total_questions_attempted_with_skipped', 0)
        player.average_time_per_question = quiz_results.get('average_time_per_question', 0)
        player.average_time_per_question_with_skipped = quiz_results.get('average_time_per_question_with_skipped', 0)
        player.correct_answers_count = quiz_results.get('correct_answers_count', 0)
        player.wrong_answers_count = quiz_results.get('wrong_answers_count', 0)
        player.skipped_questions_count = quiz_results.get('skipped_questions_count', 0)
    else:
        # If no competition_results, try to get from other participant.vars
        player.quiz_score = player.participant.vars.get('score', 0)
        player.quiz_questions_attempted = player.participant.vars.get('questions_attempted', 0)
        player.correct_answers_count = player.participant.vars.get('correct_answers_count', 0)
        player.wrong_answers_count = player.participant.vars.get('wrong_answers_count', 0)
        player.skipped_questions_count = player.participant.vars.get('skipped_questions_count', 0)
        player.total_questions_attempted_with_skipped = player.participant.vars.get(
            'total_questions_attempted_with_skipped', 0)
        player.average_time_per_question = player.participant.vars.get('average_time_per_question', 0)
        player.average_time_per_question_with_skipped = player.participant.vars.get(
            'average_time_per_question_with_skipped', 0)
        player.quiz_is_winner = player.quiz_score >= 11  # Use threshold

        # Calculate total time (if needed)
        if not hasattr(player, 'quiz_total_time') or player.quiz_total_time == 0:
            total_time_spent = 0
            # Try to accumulate time from each round
            for i in range(1, 51):  # Assume maximum 50 rounds
                round_time = player.participant.vars.get(f'question_time_spent_round_{i}', 0)
                if round_time > 0:
                    total_time_spent += round_time

            # If accumulated time is 0, try to calculate using start and end time
            if total_time_spent == 0:
                quiz_start = player.participant.vars.get('quiz_start_time')
                quiz_end = player.participant.vars.get('quiz_end_time', time.time())
                if quiz_start:
                    total_time_spent = quiz_end - quiz_start

            player.quiz_total_time = total_time_spent

    # Other data
    player.results_message = player.participant.vars.get('results_message', '')
    player.competition_result = player.participant.vars.get('competition_result', '')

    return player


class Player(BasePlayer):
    prolific_id = models.StringField(default="", blank=True)

    quiz_score = models.FloatField(initial=0)
    quiz_questions_attempted = models.IntegerField(initial=0)
    quiz_is_winner = models.BooleanField(initial=False)
    quiz_total_time = models.FloatField(initial=0)

    # Add these new fields
    results_message = models.StringField(blank=True)  # Store formatted result message
    total_questions_attempted_with_skipped = models.IntegerField(initial=0)
    average_time_per_question = models.FloatField(initial=0)
    average_time_per_question_with_skipped = models.FloatField(initial=0)

    # Add answer statistics fields
    correct_answers_count = models.IntegerField(initial=0)  # Total correct answers
    wrong_answers_count = models.IntegerField(initial=0)  # Total wrong answers
    skipped_questions_count = models.IntegerField(initial=0)  # Total skipped questions

    # Add competition_result field
    competition_result = models.StringField(blank=True)  # Competition result description

    introduction_time = models.FloatField(initial=0)
    enjoyment_time = models.FloatField(initial=0)
    voluntary_time = models.FloatField(initial=0)
    iq_quiz_willingness_time = models.FloatField(initial=0)
    labor_survey_time = models.FloatField(initial=0)
    success_belief_time = models.FloatField(initial=0)

    enjoyment = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    emotion_stress = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    # REMOVED: emotion_tension field

    emotion_excitement = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    emotion_satisfaction = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    emotion_embarrassment = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    emotion_anxiety = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    emotion_time = models.FloatField(initial=0)

    likelihood_voluntary = models.IntegerField(
        choices=[
            [1, 'Not at all'],
            [2, 'Slightly'],
            [3, 'Somewhat'],
            [4, 'Neutral'],
            [5, 'Moderately'],
            [6, 'Very'],
            [7, 'Extremely']
        ],
        blank=True
    )

    participate_020 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_040 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_060 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_080 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_100 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_120 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_140 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_160 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_180 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_200 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_250 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_300 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)
    participate_500 = models.StringField(choices=["Yes", "No"], widget=widgets.RadioSelectHorizontal)

    labor_estimate = models.StringField(choices=[
        ('20', 'Around 20 jobs'),
        ('80', 'Around 80 jobs')
    ], widget=widgets.RadioSelect)

    success_belief = models.StringField(choices=[
        ('strongly_agree_1', 'Agree strongly with statement 1'),
        ('agree_1', 'Agree with statement 1'),
        ('agree_2', 'Agree with statement 2'),
        ('strongly_agree_2', 'Agree strongly with statement 2'),
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'),
        ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'),
        ('9', '9'), ('10', '10')
    ], widget=widgets.RadioSelect)


    app3_completed = models.BooleanField(default=False, doc="Completed A1_GT_3_Survey")



# Pages

class Introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.introduction_time = time.time() - start_time
        update_progress(player, 'Introduction')

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        # Return dictionary with progress percent and threshold constants
        return {
            'progress_percent': get_progress(player, 'Introduction')['progress_percent'],
            'quiz_penalty_threshold': C.QUIZ_PENALTY_THRESHOLD,
            'quiz_penalty_amount': C.QUIZ_PENALTY_AMOUNT,
            'base_payment': C.BASE_PAYMENT,
            'competition_result': player.competition_result
        }


class EnjoymentSurvey(Page):
    form_model = 'player'
    form_fields = ['enjoyment']

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        progress_data = get_progress(player, 'EnjoymentSurvey')
        progress_data['competition_result'] = player.competition_result
        return progress_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.enjoyment_time = time.time() - start
        update_progress(player, 'EnjoymentSurvey')


class EmotionSurvey(Page):
    form_model = 'player'
    form_fields = [
        'emotion_stress',
        # REMOVED: 'emotion_tension',
        'emotion_excitement',
        'emotion_satisfaction',
        'emotion_embarrassment',
        'emotion_anxiety'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        progress_data = get_progress(player, 'EmotionSurvey')
        progress_data['competition_result'] = player.competition_result
        return progress_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.emotion_time = time.time() - start
        update_progress(player, 'EmotionSurvey')


class VoluntaryLikelihood(Page):
    form_model = 'player'
    form_fields = ['likelihood_voluntary']

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        progress_data = get_progress(player, 'VoluntaryLikelihood')
        progress_data['competition_result'] = player.competition_result
        return progress_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.voluntary_time = time.time() - start
        update_progress(player, 'VoluntaryLikelihood')


class NewIQQuizWillingness(Page):
    form_model = 'player'
    form_fields = [
        'participate_020', 'participate_040', 'participate_060', 'participate_080',
        'participate_100', 'participate_120', 'participate_140', 'participate_160',
        'participate_180', 'participate_200', 'participate_250', 'participate_300', 'participate_500'
    ]

    def vars_for_template(player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        return {
            'payment_options': ["$0.20", "$0.40", "$0.60", "$0.80", "$1.00", "$1.20",
                                "$1.40", "$1.60", "$1.80", "$2.00", "$2.50", "$3.00", "$5.00"],
            'progress_percent': get_progress(player, 'NewIQQuizWillingness')['progress_percent'],
            'min_correct_questions': C.MIN_CORRECT_QUESTIONS,
            'competition_result': player.competition_result
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.iq_quiz_willingness_time = time.time() - start
        update_progress(player, 'NewIQQuizWillingness')


class LaborSurvey(Page):
    form_model = 'player'
    form_fields = ['labor_estimate']

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        progress_data = get_progress(player, 'LaborSurvey')
        progress_data['competition_result'] = player.competition_result
        return progress_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.labor_survey_time = time.time() - start
        update_progress(player, 'LaborSurvey')


class WVSPage(Page):
    form_model = 'player'
    form_fields = ['success_belief']

    def vars_for_template(player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically get quiz data
        get_quiz_data_for_player(player)

        progress_data = get_progress(player, 'WVSPage')
        progress_data['competition_result'] = player.competition_result
        return progress_data

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.success_belief_time = time.time() - start
        update_progress(player, 'WVSPage')
        player.participant.vars['app1_completed'] = True

        # Set App3 completion flag
        player.participant.vars['app3_completed'] = True

        # Also save to Player model field
        player.app3_completed = True  # Need to add this field in Player class


page_sequence = [
    Introduction, EnjoymentSurvey, EmotionSurvey, VoluntaryLikelihood,
    NewIQQuizWillingness, LaborSurvey, WVSPage
]