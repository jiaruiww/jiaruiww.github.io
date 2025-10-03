from otree.api import *
import random
import sys
import os
import time

# Try to import global functions (safe fallback)
try:
    from global_functions import get_progress, update_progress, initialize_progress
except ImportError:
    # Retain backup implementation in case import fails
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


class C(BaseConstants):
    NAME_IN_URL = 'A3_LT_4_Decision_P'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ROLE1 = 'Role 1'
    ROLE2 = 'Role 2'

    APP3_PAGES = 6  # A3_LT_3_Survey page count
    APP4_PAGES = 4  # Current application page count
    TOTAL_PROGRESS_UNITS = APP3_PAGES + APP4_PAGES  # = 12

    # Understanding check option constants
    UNDERSTANDING_CHECK_CHOICES = [
        ('$0.80', '$0.80'),
        ('$0.90', '$0.90'),
        ('$0.50', '$0.50'),
        ('$0.40', '$0.40'),
    ]

    # Belief elicitation choice constants
    BELIEF_PERCENTAGE_CHOICES = [
        (5, '0-10%'),
        (15, '11-20%'),
        (25, '21-30%'),
        (35, '31-40%'),
        (45, '41-50%'),
        (55, '51-60%'),
        (65, '61-70%'),
        (75, '71-80%'),
        (85, '81-90%'),
        (95, '91-100%'),
    ]


class Subsession(BaseSubsession):
    role1_count = models.IntegerField(initial=0)
    role2_count = models.IntegerField(initial=0)

    def creating_session(self):
        # Initialize role counters
        self.role1_count = self.session.vars.get('role1_count', 0)
        self.role2_count = self.session.vars.get('role2_count', 0)

        for p in self.get_players():
            initialize_progress(p)
            # If APP3 is completed, continue progress
            if p.participant.vars.get('app3_completed', False):
                p.participant.vars['current_progress'] = C.APP3_PAGES

            # Save Prolific ID
            if 'prolific_id' in p.participant.vars:
                p.prolific_id = p.participant.vars['prolific_id']
            elif p.participant.label:
                p.prolific_id = p.participant.label
                # Ensure it's also stored in participant.vars
                p.participant.vars['prolific_id'] = p.participant.label

            # Get quiz score from previous app
            p.quiz_score = p.participant.vars.get('score', 0)

            # Get paired partner data
            if 'paired_partner_id' in p.participant.vars:
                try:
                    p.paired_partner_id = int(p.participant.vars['paired_partner_id'])
                except (ValueError, TypeError):
                    # If unable to convert to integer, set to default value
                    p.paired_partner_id = 0
                    print(
                        f"Error converting paired_partner_id for player {p.id_in_group}: {p.participant.vars['paired_partner_id']}")

            # Add debug output
            print(
                f"Player {p.id_in_group} data: prolific_id={p.prolific_id}, quiz_score={p.quiz_score}, paired_partner_id={p.paired_partner_id}")

            # Role assignment logic
            if 'assigned_role' in p.participant.vars:
                p.assigned_role = p.participant.vars['assigned_role']
                p.debug_role_assignment = f"Using existing role assignment: {p.assigned_role}"
            else:
                if self.role1_count <= self.role2_count:
                    p.assigned_role = C.ROLE1
                    self.role1_count += 1
                else:
                    p.assigned_role = C.ROLE2
                    self.role2_count += 1

                p.participant.vars['assigned_role'] = p.assigned_role
                p.debug_role_assignment = f"New balanced role assignment: {p.assigned_role}, Role1 count: {self.role1_count}, Role2 count: {self.role2_count}"

            # Save updated counters
            self.session.vars['role1_count'] = self.role1_count
            self.session.vars['role2_count'] = self.role2_count

            # Initialize understanding check attempt tracking fields
            p.understanding_check_attempts = 0
            p.understanding_check_attempt_history = ""


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField(default="", blank=True)
    paired_partner_id = models.IntegerField(initial=0)
    quiz_score = models.FloatField(initial=0)

    assigned_role = models.StringField(
        doc="Player's assigned role: Role 1 or Role 2",
        default=C.ROLE1,
        initial=C.ROLE1
    )

    decision = models.StringField(
        choices=['Put into pool', 'Keep the money'],
        verbose_name="Your decision:",
        doc="Player's choice between putting money into pool or keeping it"
    )

    # Modified belief_percentage field to match HTML choices
    belief_percentage = models.IntegerField(
        choices=C.BELIEF_PERCENTAGE_CHOICES,
        doc="Belief about percentage of participants who choose to keep the money",
        verbose_name="Your belief (percentage):",
        blank=True,
        null=True
    )

    understanding_check = models.StringField(
        verbose_name="",
        choices=C.UNDERSTANDING_CHECK_CHOICES,
        widget=widgets.RadioSelect,
        doc="Understanding check question"
    )

    # Understanding check attempt tracking fields
    understanding_check_attempts = models.IntegerField(
        initial=0,
        doc="Count of attempts on understanding check question"
    )

    understanding_check_attempt_history = models.StringField(
        initial="",
        doc="Record of all understanding check attempts"
    )

    understanding_check_correct = models.BooleanField(
        initial=False,
        doc="Whether the understanding check was answered correctly"
    )

    debug_role_assignment = models.StringField(default="No role assigned")

    # Add time tracking fields
    introduction_time = models.FloatField(initial=0)  # Introduction page time
    decision_time = models.FloatField(initial=0)  # Decision page time
    belief_time = models.FloatField(initial=0)  # BeliefElicitation page time
    dictator_game_time = models.FloatField(initial=0)  # DictatorGame page time

    app4_completed = models.BooleanField(default=False, doc="Completed A1_GT_4_Decision_P")

    # Dictator game allocation fields - improved version

    # Keep original slider value for form handling (backward compatible)
    allocation_amount = models.IntegerField(
        min=0,
        max=100,
        initial=50,
        doc="Raw slider value: Amount allocated to the other person (0-100)",
        verbose_name="Your allocation to the other person:"
    )

    # New: Explicitly record amount allocated to self
    self_amount = models.IntegerField(
        min=0,
        max=100,
        initial=50,
        doc="Amount the player keeps for themselves in dictator game ($0-$100)",
        verbose_name="Amount kept for yourself:"
    )

    # New: Explicitly record amount allocated to other person
    other_amount = models.IntegerField(
        min=0,
        max=100,
        initial=50,
        doc="Amount the player allocates to the other person in dictator game ($0-$100)",
        verbose_name="Amount given to other person:"
    )


class Introduction(Page):
    form_model = 'player'
    form_fields = ['understanding_check']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure critical data is passed from previous app
        if not player.field_maybe_none('quiz_score'):
            if 'score' in player.participant.vars:
                player.quiz_score = player.participant.vars['score']
            elif 'quiz_score' in player.participant.vars:
                player.quiz_score = player.participant.vars['quiz_score']

        if not player.field_maybe_none('prolific_id') and 'prolific_id' in player.participant.vars:
            player.prolific_id = player.participant.vars['prolific_id']

        # Only return progress update, remove non-existent constant references
        vars_dict = {}
        vars_dict.update(update_progress(player, 'Introduction_App2'))
        return vars_dict

    def error_message(player, values):
        answer = values.get('understanding_check')
        if not answer:
            return {'understanding_check': 'Please select an answer.'}

        if answer != '$0.40':
            # Record wrong answer and increment attempt count
            player.understanding_check_attempts += 1

            # Record wrong answer history
            if player.understanding_check_attempt_history:
                player.understanding_check_attempt_history += f",{answer}"
            else:
                player.understanding_check_attempt_history = answer

            return {
                'understanding_check': 'Your answer is incorrect. Please review the instructions and try again.'
            }

    def before_next_page(player, timeout_happened):
        # If correct answer, also record and increment attempt count
        if player.understanding_check == '$0.40':
            player.understanding_check_attempts += 1

            # Record correct answer
            if player.understanding_check_attempt_history:
                player.understanding_check_attempt_history += f",{player.understanding_check}"
            else:
                player.understanding_check_attempt_history = player.understanding_check

            # Mark as answered correctly
            player.understanding_check_correct = True

        # Calculate page time
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.introduction_time = time.time() - start_time

    def js_vars(player):
        return {
            'custom_error_message': "Incorrect. Please review the instructions and try again."
        }


class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Ensure data continuity
        if not player.field_maybe_none('quiz_score'):
            player.quiz_score = player.participant.vars.get('score', 0)

        role = player.assigned_role if player.assigned_role else C.ROLE1
        partner_data = ""

        # Try to get paired partner data
        if player.paired_partner_id > 0 or 'paired_partner_id' in player.participant.vars:
            if player.paired_partner_id == 0 and 'paired_partner_id' in player.participant.vars:
                try:
                    player.paired_partner_id = int(player.participant.vars['paired_partner_id'])
                except (ValueError, TypeError):
                    player.paired_partner_id = 0

            if player.paired_partner_id > 0:
                partner = next((p for p in player.subsession.get_players()
                                if p.participant.id_in_session == player.paired_partner_id), None)
                if partner:
                    partner_data = f"Quiz Score: {partner.quiz_score}"

        # Only return actually needed variables, remove non-existent constant references
        vars_dict = {
            'role': role,
            'partner_data': partner_data
        }

        vars_dict.update(update_progress(player, 'Decision_App2'))
        return vars_dict

    def error_message(player, values):
        # Reinforce server-side validation
        if 'decision' not in values or values['decision'] is None:
            return 'Please select either \'Put into pool\' or \'Keep the money\' to proceed.'

        # Ensure the selection is a valid option
        if values['decision'] not in ['Put into pool', 'Keep the money']:
            return 'Invalid choice. Please select either \'Put into pool\' or \'Keep the money\'.'

    def before_next_page(player, timeout_happened):
        # Calculate page time
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.decision_time = time.time() - start_time

        # Additional data consistency check - set a default value if decision is still invalid
        if not player.field_maybe_none('decision') or player.decision not in ['Put into pool', 'Keep the money']:
            player.decision = 'Put into pool'  # Set default to ensure data integrity


class BeliefElicitation(Page):
    form_model = 'player'
    form_fields = ['belief_percentage']

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        try:
            player.assigned_role = C.ROLE1 if not player.field_maybe_none('assigned_role') else player.assigned_role
            player.debug_role_assignment = f"Force-set role in BeliefElicitation page: {player.assigned_role}"
        except:
            player.assigned_role = C.ROLE1
            player.debug_role_assignment = "Emergency fallback in BeliefElicitation page"

        role = player.assigned_role or C.ROLE1

        # Only return actually needed variables, remove non-existent constant references
        vars_dict = {
            'role': role,
        }

        vars_dict.update(update_progress(player, 'BeliefElicitation_App2'))
        return vars_dict

    def before_next_page(player, timeout_happened):
        # Calculate page time
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.belief_time = time.time() - start_time

    def error_message(player, values):
        # Strengthen server-side validation
        if 'belief_percentage' not in values or values['belief_percentage'] is None:
            return 'Please select a percentage range to continue.'

        try:
            percentage = int(values['belief_percentage'])
            # Check if it's a valid choice value
            valid_choices = [choice[0] for choice in C.BELIEF_PERCENTAGE_CHOICES]
            if percentage not in valid_choices:
                return 'Please select a valid percentage range.'
        except (ValueError, TypeError):
            return 'Please select a valid percentage range.'


class DictatorGame(Page):
    form_model = 'player'
    form_fields = ['allocation_amount']  # Keep form field unchanged

    def vars_for_template(player):
        # Record page start time
        player.participant.vars['page_start_time'] = time.time()

        # Only return actually needed variables
        vars_dict = {}
        vars_dict.update(update_progress(player, 'DictatorGame_App2'))
        return vars_dict

    def before_next_page(player, timeout_happened):
        # Calculate page time
        start_time = player.participant.vars.get('page_start_time', time.time())
        player.dictator_game_time = time.time() - start_time

        # New improved logic: explicitly calculate and store both amounts

        # allocation_amount represents the amount given to the other person (slider value)
        other_amount = player.allocation_amount
        your_amount = 100 - player.allocation_amount

        # Store in explicit database fields
        player.other_amount = other_amount
        player.self_amount = your_amount

        # Also maintain storage in participant.vars (for cross-app data passing, backward compatible)
        player.participant.vars['dictator_other_amount'] = other_amount
        player.participant.vars['dictator_your_amount'] = your_amount
        player.participant.vars['dictator_self_amount'] = your_amount  # Add alias for consistency

        # Optional: add validation to ensure amounts sum to 100
        assert player.self_amount + player.other_amount == 100, f"Allocation amounts must sum to 100, got self={player.self_amount}, other={player.other_amount}"

        # Set App4 completion flag
        player.participant.vars['app4_completed'] = True
        player.app4_completed = True


    def error_message(player, values):
        # Validate allocation amount
        if 'allocation_amount' not in values or values['allocation_amount'] is None:
            return 'Please use the slider to make your allocation.'

        try:
            amount = int(values['allocation_amount'])
            if amount < 0 or amount > 100:
                return 'Please select a valid allocation between $0 and $100.'
        except (ValueError, TypeError):
            return 'Please select a valid allocation amount.'


page_sequence = [Introduction, Decision, BeliefElicitation, DictatorGame]