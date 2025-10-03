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
    NAME_IN_URL = 'A1_GT_3_Survey'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # Updated to include EmotionSurvey and LaborSurvey pages
    TOTAL_PROGRESS_UNITS = 6  # Introduction + EnjoymentSurvey + EmotionSurvey + VoluntaryLikelihood + NewIQQuizWillingness + LaborSurvey + WVSPage


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
    """Dynamically retrieve quiz data, getting latest data from participant.vars each time"""

    # Basic information
    player.prolific_id = player.participant.vars.get('prolific_id', '')

    # Get data from competition_results
    quiz_results = player.participant.vars.get('competition_results', {})

    if quiz_results:
        player.quiz_score = quiz_results.get('player_score', 0)
        player.quiz_questions_attempted = quiz_results.get('total_questions_attempted', 0)
        player.quiz_is_winner = quiz_results.get('is_winner', False)
        player.quiz_total_time = quiz_results.get('total_time_spent', 0)
        player.competition_result = quiz_results.get('result_message', '')
        player.opponent_score = quiz_results.get('opponent_score', None)
        player.total_questions_attempted_with_skipped = quiz_results.get('total_questions_attempted_with_skipped', 0)
        player.average_time_per_question = quiz_results.get('average_time_per_question', 0)
        player.average_time_per_question_with_skipped = quiz_results.get('average_time_per_question_with_skipped', 0)

        # Debug output
        print(f"A1_GT Survey - Player {player.id_in_group} data from competition_results:")
        print(f"  - Score: {player.quiz_score}, Winner: {player.quiz_is_winner}")
        print(f"  - Opponent score: {player.opponent_score}")

    else:
        # If no competition_results, try to get from other participant.vars
        player.quiz_score = player.participant.vars.get('score', 0)
        player.quiz_questions_attempted = player.participant.vars.get('questions_attempted', 0)
        player.quiz_total_time = player.participant.vars.get('quiz_total_time', 0)
        player.competition_result = player.participant.vars.get('competition_result', '')
        player.opponent_score = player.participant.vars.get('opponent_score', None)
        player.total_questions_attempted_with_skipped = player.participant.vars.get(
            'total_questions_attempted_with_skipped', 0)
        player.average_time_per_question = player.participant.vars.get('average_time_per_question', 0)
        player.average_time_per_question_with_skipped = player.participant.vars.get(
            'average_time_per_question_with_skipped', 0)

        # Calculate total time (if needed)
        if player.quiz_total_time == 0:
            total_time_spent = 0
            # Try to accumulate time from each round
            for i in range(1, 51):  # Assume max 50 rounds
                round_time = player.participant.vars.get(f'question_time_spent_round_{i}', 0)
                if round_time > 0:
                    total_time_spent += round_time

            # If accumulated time is 0, try using start and end times
            if total_time_spent == 0:
                quiz_start = player.participant.vars.get('quiz_start_time')
                quiz_end = player.participant.vars.get('quiz_end_time', time.time())
                if quiz_start:
                    total_time_spent = quiz_end - quiz_start

            player.quiz_total_time = total_time_spent

        # Debug output
        print(f"A1_GT Survey - Player {player.id_in_group} data from direct participant.vars:")
        print(f"  - Score: {player.quiz_score}")
        print(f"  - Opponent score: {player.opponent_score}")

    # Detailed answer statistics (A1_GT specific competition data)
    player.correct_answers_count = player.participant.vars.get('correct_answers_count', 0)
    player.wrong_answers_count = player.participant.vars.get('wrong_answers_count', 0)
    player.skipped_questions_count = player.participant.vars.get('skipped_questions_count', 0)

    # Pairing related data transfer (fix type issue)
    partner_id = player.participant.vars.get('paired_partner_id')
    if partner_id:
        # Ensure partner_id is integer type
        try:
            player.paired_partner_id = int(partner_id) if partner_id else 0
        except (ValueError, TypeError):
            player.paired_partner_id = 0
    else:
        player.paired_partner_id = 0

    player.paired_partner_prolific_id = player.participant.vars.get('paired_partner_prolific_id', '')
    player.is_successfully_paired = player.participant.vars.get('is_successfully_paired', False)
    player.matching_wait_time = player.participant.vars.get('matching_wait_time', None)
    player.matching_timeout_occurred = player.participant.vars.get('matching_timeout_occurred',
                                                                   player.participant.vars.get('matching_timed_out',
                                                                                               False))

    # Tie related data transfer
    player.tie_occurred = player.participant.vars.get('tie_occurred', False)
    player.tie_random_result = player.participant.vars.get('tie_random_result', '')

    return player


class Player(BasePlayer):
    prolific_id = models.StringField(default="", blank=True)

    quiz_score = models.FloatField(initial=0)
    quiz_questions_attempted = models.IntegerField(initial=0)
    quiz_is_winner = models.BooleanField(initial=False)
    quiz_total_time = models.FloatField(initial=0)

    # Detailed answer situation fields
    correct_answers_count = models.IntegerField(initial=0)
    wrong_answers_count = models.IntegerField(initial=0)
    skipped_questions_count = models.IntegerField(initial=0)

    # Pairing related fields
    paired_partner_id = models.IntegerField(initial=0)  # Set default value to 0 instead of blank=True
    paired_partner_prolific_id = models.StringField(blank=True)
    is_successfully_paired = models.BooleanField(initial=False)
    matching_wait_time = models.FloatField(blank=True, null=True)
    matching_timeout_occurred = models.BooleanField(initial=False)

    # Competition related fields
    competition_result = models.StringField(blank=True)
    opponent_score = models.FloatField(blank=True, null=True)
    tie_occurred = models.BooleanField(initial=False)
    tie_random_result = models.StringField(blank=True)

    # Time recording fields
    introduction_time = models.FloatField(initial=0)
    enjoyment_time = models.FloatField(initial=0)
    emotion_time = models.FloatField(initial=0)  # EmotionSurvey time
    voluntary_time = models.FloatField(initial=0)
    iq_quiz_willingness_time = models.FloatField(initial=0)
    labor_survey_time = models.FloatField(initial=0)  # LaborSurvey time (replaces computer_sales_time)
    success_belief_time = models.FloatField(initial=0)

    total_questions_attempted_with_skipped = models.IntegerField(initial=0)
    average_time_per_question_with_skipped = models.FloatField(initial=0)
    average_time_per_question = models.FloatField(initial=0)

    # Survey question fields
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

    # Emotion survey fields
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

    # Labor survey fields (replaces sales_estimate)
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

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'Introduction')


class EnjoymentSurvey(Page):
    form_model = 'player'
    form_fields = ['enjoyment']

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'EnjoymentSurvey')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.enjoyment_time = time.time() - start
        update_progress(player, 'EnjoymentSurvey')


# EmotionSurvey page
class EmotionSurvey(Page):
    form_model = 'player'
    form_fields = [
        'emotion_stress',
        'emotion_excitement',
        'emotion_satisfaction',
        'emotion_embarrassment',
        'emotion_anxiety'
    ]

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'EmotionSurvey')

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

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'VoluntaryLikelihood')

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

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return {
            'payment_options': ["$0.20", "$0.40", "$0.60", "$0.80", "$1.00", "$1.20",
                                "$1.40", "$1.60", "$1.80", "$2.00", "$2.50", "$3.00", "$5.00"],
            'progress_percent': get_progress(player, 'NewIQQuizWillingness')['progress_percent']
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.iq_quiz_willingness_time = time.time() - start
        update_progress(player, 'NewIQQuizWillingness')


# LaborSurvey page (replaces ComputerSalesSurvey)
class LaborSurvey(Page):
    form_model = 'player'
    form_fields = ['labor_estimate']

    @staticmethod
    def vars_for_template(player: Player):
        player.participant.vars['page_start_time'] = time.time()

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'LaborSurvey')

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

        # Dynamically retrieve quiz data
        get_quiz_data_for_player(player)

        return get_progress(player, 'WVSPage')

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        start = player.participant.vars.get('page_start_time', time.time())
        player.success_belief_time = time.time() - start
        update_progress(player, 'WVSPage')
        # Set App3 completion flag
        player.participant.vars['app3_completed'] = True

        # Also save to Player model field
        player.app3_completed = True


# Updated page sequence
page_sequence = [
    Introduction, EnjoymentSurvey, EmotionSurvey, VoluntaryLikelihood,
    NewIQQuizWillingness, LaborSurvey, WVSPage
]
