from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = 'A3_LT_2_Quiz'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 50
    TOTAL_TIME = 240
    INITIAL_SCORE = 0

    RETURN_CODE = 'CPUU0BOU'

    QUESTION_IMAGES = {
        1: 'Q2cropped.png', 2: 'Q3cropped.png', 3: 'Q20cropped.png', 4: 'Q21cropped.png',
        5: 'Q23cropped.png', 6: 'Q4cropped.png', 7: 'Q25cropped.png', 8: 'Q5cropped.png',
        9: 'Q45cropped.png', 10: 'Q7cropped.png', 11: 'Q13cropped.png', 12: 'Q8cropped.png',
        13: 'Q11cropped.png', 14: 'Q18cropped.png', 15: 'Q12cropped.png', 16: 'Q17cropped.png',
        17: 'Q16cropped.png', 18: 'Q10cropped.png', 19: 'Q15cropped.png', 20: 'Q9cropped.png',
        21: 'Q22cropped.png', 22: 'Q6cropped.png', 23: 'Q46cropped.png', 24: 'Q24cropped.png',
        25: 'Q26cropped.png', 26: 'Q27cropped.png', 27: 'Q28cropped.png', 28: 'Q29cropped.png',
        29: 'Q30cropped.png', 30: 'Q31cropped.png', 31: 'Q32cropped.png', 32: 'Q33cropped.png',
        33: 'Q14cropped.png', 34: 'Q19cropped.png', 35: 'Q34cropped.png', 36: 'Q1cropped.png',
        37: 'Q35cropped.png', 38: 'Q36cropped.png', 39: 'Q37cropped.png', 40: 'Q38cropped.png',
        41: 'Q39cropped.png', 42: 'Q40cropped.png', 43: 'Q41cropped.png', 44: 'Q43cropped.png',
        45: 'Q44cropped.png', 46: 'Q42cropped.png', 47: 'Q47cropped.png', 48: 'Q48cropped.png',
        49: 'Q49cropped.png', 50: 'Q50cropped.png'
    }

    CHOICE_IMAGES = {
        1: 'Q2cropped_sol.png', 2: 'Q3cropped_sol.png', 3: 'Q20cropped_sol.png', 4: 'Q21cropped_sol.png',
        5: 'Q23cropped_sol.png', 6: 'Q4cropped_sol.png', 7: 'Q25cropped_sol.png', 8: 'Q5cropped_sol.png',
        9: 'Q45cropped_sol.png', 10: 'Q7cropped_sol.png', 11: 'Q13cropped_sol.png', 12: 'Q8cropped_sol.png',
        13: 'Q11cropped_sol.png', 14: 'Q18cropped_sol.png', 15: 'Q12cropped_sol.png', 16: 'Q17cropped_sol.png',
        17: 'Q16cropped_sol.png', 18: 'Q10cropped_sol.png', 19: 'Q15cropped_sol.png', 20: 'Q9cropped_sol.png',
        21: 'Q22cropped_sol.png', 22: 'Q6cropped_sol.png', 23: 'Q46cropped_sol.png', 24: 'Q24cropped_sol.png',
        25: 'Q26cropped_sol.png', 26: 'Q27cropped_sol.png', 27: 'Q28cropped_sol.png', 28: 'Q29cropped_sol.png',
        29: 'Q30cropped_sol.png', 30: 'Q31cropped_sol.png', 31: 'Q32cropped_sol.png', 32: 'Q33cropped_sol.png',
        33: 'Q14cropped_sol.png', 34: 'Q19cropped_sol.png', 35: 'Q34cropped_sol.png', 36: 'Q1cropped_sol.png',
        37: 'Q35cropped_sol.png', 38: 'Q36cropped_sol.png', 39: 'Q37cropped_sol.png', 40: 'Q38cropped_sol.png',
        41: 'Q39cropped_sol.png', 42: 'Q40cropped_sol.png', 43: 'Q41cropped_sol.png', 44: 'Q43cropped_sol.png',
        45: 'Q44cropped_sol.png', 46: 'Q42cropped_sol.png', 47: 'Q47cropped_sol.png', 48: 'Q48cropped_sol.png',
        49: 'Q49cropped_sol.png', 50: 'Q50cropped_sol.png'
    }

    CORRECT_ANSWERS = {
        1: 2, 2: 3, 3: 1, 4: 3, 5: 3, 6: 2, 7: 4, 8: 3, 9: 4, 10: 1,
        11: 3, 12: 4, 13: 1, 14: 3, 15: 2, 16: 1, 17: 2, 18: 2, 19: 1, 20: 2,
        21: 1, 22: 2, 23: 1, 24: 1, 25: 1, 26: 3, 27: 1, 28: 4, 29: 1, 30: 3,
        31: 1, 32: 4, 33: 2, 34: 1, 35: 1, 36: 1, 37: 4, 38: 1, 39: 1, 40: 4,
        41: 1, 42: 3, 43: 2, 44: 1, 45: 2, 46: 1, 47: 1, 48: 1, 49: 2, 50: 1
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number > 1:
            self.group_like_round(1)


class Group(BaseGroup):
    quiz_start_timestamp = models.FloatField(initial=0)
    both_players_ready = models.BooleanField(initial=False)

    def handle_tie(self):
        """Handle tie situations, ensuring one player wins and one loses"""
        players = self.get_players()
        if len(players) != 2:
            return

        p1, p2 = players
        random.seed(p1.id_in_group)
        winner_idx = random.randint(0, 1)

        if winner_idx == 0:
            p1.is_winner = True
            p1.tie_occurred = True
            p1.tie_random_result = "Won by random selection"
            p1.competition_result = "It's a tie. You are randomly selected as the top performer."
            p2.is_winner = False
            p2.tie_occurred = True
            p2.tie_random_result = "Lost by random selection"
            p2.competition_result = "It's a tie. You are randomly selected as the bottom performer."
        else:
            p1.is_winner = False
            p1.tie_occurred = True
            p1.tie_random_result = "Lost by random selection"
            p1.competition_result = "It's a tie. You are randomly selected as the bottom performer."
            p2.is_winner = True
            p2.tie_occurred = True
            p2.tie_random_result = "Won by random selection"
            p2.competition_result = "It's a tie. You are randomly selected as the top performer."

        for p in players:
            opponent = p.get_others_in_group()[0]
            p.participant.vars['competition_results'] = {
                'total_questions': C.NUM_ROUNDS,
                'total_questions_attempted': p.participant.vars.get('questions_attempted', 0),
                'total_questions_attempted_with_skipped': p.participant.vars.get('total_questions_attempted_with_skipped', 0),
                'player_score': p.participant.vars.get('score', C.INITIAL_SCORE),
                'opponent_score': opponent.participant.vars.get('score', C.INITIAL_SCORE),
                'result_message': p.competition_result,
                'is_winner': p.is_winner,
                'total_time_spent': p.total_time_spent,
                'average_time_per_question': p.participant.vars.get('average_time_per_question', 0),
                'average_time_per_question_with_skipped': p.participant.vars.get('average_time_per_question_with_skipped', 0)
            }


class Player(BasePlayer):
    prolific_id = models.StringField(default="", blank=True)
    user_answer = models.IntegerField(
        label="Your Answer",
        choices=[[1, 'A'], [2, 'B'], [3, 'C'], [4, 'D']],
        widget=widgets.RadioSelect,
        blank=True,
        field_maybe_none=True
    )
    is_answer_correct = models.BooleanField(initial=False)
    is_answer_wrong = models.BooleanField(initial=False)
    question_time_spent = models.FloatField(initial=0)
    final_score = models.FloatField(initial=C.INITIAL_SCORE)
    is_winner = models.BooleanField(initial=False)
    total_questions_attempted = models.IntegerField(initial=0)
    total_time_spent = models.FloatField(initial=0)
    correct_answers_count = models.IntegerField(initial=0)
    wrong_answers_count = models.IntegerField(initial=0)
    skipped_questions_count = models.IntegerField(initial=0)
    paired_partner_id = models.StringField(blank=True)
    paired_partner_prolific_id = models.StringField(blank=True)
    is_successfully_paired = models.BooleanField(initial=False)
    matching_wait_time = models.FloatField(blank=True, null=True)
    matching_timeout_occurred = models.BooleanField(initial=False)
    competition_result = models.StringField(blank=True)
    opponent_score = models.FloatField(blank=True, null=True)
    tie_occurred = models.BooleanField(initial=False)
    tie_random_result = models.StringField(blank=True)
    total_questions_attempted_with_skipped = models.IntegerField(initial=0)
    average_time_per_question = models.FloatField(initial=0)
    average_time_per_question_with_skipped = models.FloatField(initial=0)
    time_jump_occurred = models.BooleanField(initial=False)
    time_jump_detection_method = models.StringField(blank=True)
    real_quiz_duration = models.FloatField(initial=0)
    last_active_timestamp = models.FloatField(initial=0)
    session_interruption_detected = models.BooleanField(initial=False)
    total_interruption_time = models.FloatField(initial=0)
    quiz_completion_method = models.StringField(blank=True)


def group_by_arrival_time_method(subsession, waiting_players):
    if hasattr(waiting_players, 'get_players'):
        players_to_check = waiting_players.get_players()
    else:
        players_to_check = waiting_players

    active_players = []
    for p in players_to_check:
        if not p.participant.vars.get('matching_timed_out', False):
            active_players.append(p)

    if len(active_players) >= 2:
        return active_players[:2]
    return None


class MatchingWaitPage(WaitPage):
    group_by_arrival_time = True
    template_name = 'A3_LT_2_Quiz/MatchingWaitPage.html'

    @staticmethod
    def js_vars(player: Player):
        current_time = time.time()
        start_time = player.participant.vars.get('wait_page_start_time', current_time)
        elapsed_time = current_time - start_time
        timeout_duration = 300
        remaining_time = max(0, timeout_duration - elapsed_time)

        if player.group and player.group.both_players_ready:
            return {
                'timeout': remaining_time,
                'both_ready': True,
                'redirect_to_quiz': True
            }
        return {'timeout': remaining_time}

    @staticmethod
    def vars_for_template(player: Player):
        current_time = time.time()
        start_time = player.participant.vars.get('wait_page_start_time', current_time)
        elapsed_time = current_time - start_time
        timeout_duration = 300
        timeout_happened = elapsed_time >= timeout_duration

        if timeout_happened:
            player.participant.vars['matching_timed_out'] = True
            player.participant.vars['timeout_message_shown'] = True
            player.is_successfully_paired = False
            player.matching_timeout_occurred = True
            player.matching_wait_time = elapsed_time
            player.competition_result = "Not paired due to timeout"

        is_synced = False
        redirect_url = ''
        if player.group and player.group.both_players_ready:
            is_synced = True
            redirect_url = f'/p/{player.participant.code}/A3_LT_2_Quiz/QuizPage/1/'

        return {
            'timeout_happened': timeout_happened,
            'return_code': C.RETURN_CODE,
            'is_synced': is_synced,
            'redirect_url': redirect_url
        }

    @staticmethod
    def is_displayed(player: Player):
        if 'wait_page_start_time' not in player.participant.vars:
            player.participant.vars['wait_page_start_time'] = time.time()

        if player.participant.vars.get('matching_timed_out', False):
            return True

        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(group: Group):
        players = group.get_players()
        if len(players) == 2:
            p1, p2 = players
            p1.participant.vars['paired_partner_id'] = p2.participant.id
            p2.participant.vars['paired_partner_id'] = p1.participant.id
            p1.paired_partner_id = str(p2.participant.id)
            p2.paired_partner_id = str(p1.participant.id)
            p1.is_successfully_paired = True
            p2.is_successfully_paired = True
            p1.paired_partner_prolific_id = p2.prolific_id
            p2.paired_partner_prolific_id = p1.prolific_id

            if 'wait_page_start_time' in p1.participant.vars:
                p1.matching_wait_time = time.time() - p1.participant.vars['wait_page_start_time']
            if 'wait_page_start_time' in p2.participant.vars:
                p2.matching_wait_time = time.time() - p2.participant.vars['wait_page_start_time']

            group.both_players_ready = True

        for p in players:
            if 'prolific_id' in p.participant.vars:
                p.prolific_id = p.participant.vars['prolific_id']
            elif p.participant.label:
                p.prolific_id = p.participant.label
            else:
                import random
                import string
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                fallback_id = f"session_{p.session.id}_player_{p.id_in_group}_{random_suffix}"
                p.prolific_id = fallback_id
                print(f"Warning: Participant {p.id_in_group} in session {p.session.id} is missing prolific_id, using generated ID: {fallback_id}")
                p.participant.vars['prolific_id'] = fallback_id

            p.participant.vars['score'] = C.INITIAL_SCORE
            p.participant.vars['quiz_start_time'] = time.time()
            p.participant.vars['questions_attempted'] = 0


class QuizPage(Page):
    form_model = 'player'
    form_fields = ['user_answer']
    timeout_submission = {'user_answer': None}

    @staticmethod
    def live_method(player: Player, data):
        try:
            if not hasattr(player, 'participant') or not player.participant:
                return {player.id_in_group: {'error': 'Invalid player data'}}
            if not hasattr(player, 'group') or not player.group:
                return {player.id_in_group: {'error': 'No group assigned'}}

            player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
            opponent_score = C.INITIAL_SCORE
            opponent_correct_count = 0

            try:
                others = player.get_others_in_group()
                if others and len(others) > 0:
                    opponent = others[0]
                    if opponent and hasattr(opponent, 'participant') and opponent.participant:
                        opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)
                        opponent_correct_count = opponent.participant.vars.get('correct_answers_count', 0)
            except (AttributeError, IndexError, TypeError) as e:
                print(f"Warning: Error getting opponent data for player {player.id_in_group}: {e}")

            try:
                start_time = player.participant.vars.get('quiz_start_time')
                if start_time is None:
                    start_time = time.time()
                    player.participant.vars['quiz_start_time'] = start_time
                    print(f"Warning: Missing quiz_start_time for player {player.id_in_group}, using current time")
                elapsed_time = int(time.time() - start_time)
                remaining_time = max(0, C.TOTAL_TIME - elapsed_time)
            except (TypeError, ValueError) as e:
                print(f"Error calculating time for player {player.id_in_group}: {e}")
                remaining_time = C.TOTAL_TIME

            time_expired = False
            if remaining_time <= 0 and player.round_number < C.NUM_ROUNDS:
                time_expired = True

            player_score = max(-50, min(100, float(player_score)))
            opponent_score = max(-50, min(100, float(opponent_score)))
            opponent_correct_count = max(0, min(C.NUM_ROUNDS, int(opponent_correct_count)))
            remaining_time = max(0, min(C.TOTAL_TIME, int(remaining_time)))

            response_data = {
                'player_score': player_score,
                'teammate_score': opponent_score,
                'teammate_correct_count': opponent_correct_count,
                'remaining_time': remaining_time
            }

            if time_expired:
                response_data['time_expired'] = True

            return {player.id_in_group: response_data}

        except Exception as e:
            error_msg = f"Critical error in live_method for player {getattr(player, 'id_in_group', 'unknown')}: {str(e)}"
            print(error_msg)
            return {
                getattr(player, 'id_in_group', 1): {
                    'player_score': C.INITIAL_SCORE,
                    'teammate_score': C.INITIAL_SCORE,
                    'teammate_correct_count': 0,
                    'remaining_time': C.TOTAL_TIME,
                    'time_expired': False
                }
            }

    @staticmethod
    def get_timeout_seconds(player: Player):
        start_time = player.participant.vars.get('quiz_start_time')
        if start_time is None:
            start_time = time.time()
            player.participant.vars['quiz_start_time'] = start_time
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)
        return remaining_time

    @staticmethod
    def vars_for_template(player: Player):
        if player.round_number > 1:
            player_in_round_1 = player.in_round(1)
            player.prolific_id = player_in_round_1.prolific_id

        question_image = C.QUESTION_IMAGES.get(player.round_number, "")
        choice_image = C.CHOICE_IMAGES.get(player.round_number, "")
        score = player.participant.vars.get('score', C.INITIAL_SCORE)

        others = player.get_others_in_group()
        if others:
            teammate_score = others[0].participant.vars.get('score', C.INITIAL_SCORE)
            teammate_correct_count = others[0].participant.vars.get('correct_answers_count', 0)
        else:
            teammate_score = C.INITIAL_SCORE
            teammate_correct_count = 0

        teammate_correct_count = teammate_correct_count if teammate_correct_count is not None else 0
        teammate_score = teammate_score if teammate_score is not None else C.INITIAL_SCORE

        max_display_score = 25
        if teammate_correct_count > max_display_score:
            teammate_bar_width = 100
        else:
            teammate_bar_width = max(0, int((teammate_correct_count / max_display_score) * 100))

        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)

        player.participant.vars['page_start_time'] = time.time()

        return {
            'question_number': player.round_number,
            'question_image': question_image,
            'choice_image': choice_image,
            'score': score,
            'teammate_score': teammate_score,
            'teammate_correct_count': teammate_correct_count,
            'teammate_bar_width': teammate_bar_width,
            'remaining_time': remaining_time,
            'total_time': C.TOTAL_TIME,
            'initial_score': C.INITIAL_SCORE
        }

    @staticmethod
    def is_displayed(player: Player):
        if player.participant.vars.get('go_to_results', False):
            return False
        if player.participant.vars.get('matching_timed_out', False):
            return False

        if player.round_number == 1 and 'quiz_start_time' not in player.participant.vars:
            if player.group:
                if player.group.quiz_start_timestamp == 0:
                    player.group.quiz_start_timestamp = time.time()
                player.participant.vars['quiz_start_time'] = player.group.quiz_start_timestamp

        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        time_expired = elapsed_time >= C.TOTAL_TIME

        if time_expired and player.round_number > 1:
            player.participant.vars['go_to_results'] = True
            return False

        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
            current_time = time.time()
            quiz_start_time = player.participant.vars.get('quiz_start_time', current_time)
            elapsed_time = current_time - quiz_start_time
            player.total_time_spent = elapsed_time
            player.last_active_timestamp = current_time

            accumulated_round_time = 0
            for round_num in range(1, player.round_number + 1):
                round_time_key = f'question_time_spent_round_{round_num}'
                round_time = player.participant.vars.get(round_time_key, 0)
                accumulated_round_time += round_time

            if hasattr(player, 'session_interruption_detected') and player.session_interruption_detected:
                player.real_quiz_duration = accumulated_round_time
            else:
                player.real_quiz_duration = elapsed_time

            if hasattr(player, 'session_interruption_detected') and player.session_interruption_detected:
                player.time_jump_detection_method = 'accumulated_round_time'
            elif player.last_active_timestamp > 0:
                player.time_jump_detection_method = 'last_active_timestamp'
            else:
                player.time_jump_detection_method = 'normal_elapsed_time'

            if player.participant.vars.get('go_to_results', False):
                player.quiz_completion_method = 'time_expired_jump'
            elif player.round_number == C.NUM_ROUNDS:
                player.quiz_completion_method = 'normal_completion'
            else:
                player.quiz_completion_method = 'in_progress'

            progress_percentage = (player.round_number / C.NUM_ROUNDS) * 100
            player.participant.vars['progress_percentage'] = progress_percentage
            player.participant.vars[f'active_timestamp_round_{player.round_number}'] = current_time

            if player.round_number > 1:
                prev_round = player.round_number - 1
                prev_timestamp_key = f'active_timestamp_round_{prev_round}'
                if prev_timestamp_key in player.participant.vars:
                    prev_timestamp = player.participant.vars[prev_timestamp_key]
                    time_gap = current_time - prev_timestamp
                    if time_gap > 30:
                        player.session_interruption_detected = True
                        if 'total_interruption_time' not in player.participant.vars:
                            player.participant.vars['total_interruption_time'] = 0
                        player.participant.vars['total_interruption_time'] += (time_gap - 30)
                        player.total_interruption_time = player.participant.vars['total_interruption_time']

            if not hasattr(player, 'session_interruption_detected') or player.session_interruption_detected is None:
                player.session_interruption_detected = False
            if not hasattr(player, 'total_interruption_time') or player.total_interruption_time is None:
                player.total_interruption_time = player.participant.vars.get('total_interruption_time', 0)

            player.participant.vars['current_state_snapshot'] = {
                'round_number': player.round_number,
                'timestamp': current_time,
                'total_time_spent': player.total_time_spent,
                'real_quiz_duration': player.real_quiz_duration,
                'time_jump_detection_method': player.time_jump_detection_method,
                'quiz_completion_method': player.quiz_completion_method,
                'session_interruption_detected': player.session_interruption_detected,
                'total_interruption_time': player.total_interruption_time,
                'progress_percentage': progress_percentage,
                'last_active_timestamp': player.last_active_timestamp
            }

            if player.participant.vars.get('go_to_results', False) and player.round_number > player.participant.vars.get('last_displayed_round', 0):
                return

            if not hasattr(player.participant, 'vars'):
                player.participant.vars = {}

            start_time = player.participant.vars.get('page_start_time', time.time())
            question_time = time.time() - start_time
            player.question_time_spent = question_time
            round_time_key = f'question_time_spent_round_{player.round_number}'
            player.participant.vars[round_time_key] = question_time

            current_progress = {
                'last_completed_round': player.round_number,
                'current_score': player.participant.vars.get('score', C.INITIAL_SCORE),
                'questions_attempted': player.participant.vars.get('questions_attempted', 0),
                'total_time_so_far': time.time() - player.participant.vars.get('quiz_start_time', time.time())
            }
            player.participant.vars['quiz_progress'] = current_progress

            correct_answer = C.CORRECT_ANSWERS.get(player.round_number, -1)
            user_answer = player.field_maybe_none('user_answer')

            if 'correct_answers_count' not in player.participant.vars:
                player.participant.vars['correct_answers_count'] = 0
            if 'wrong_answers_count' not in player.participant.vars:
                player.participant.vars['wrong_answers_count'] = 0
            if 'skipped_questions_count' not in player.participant.vars:
                player.participant.vars['skipped_questions_count'] = 0
            if 'questions_attempted' not in player.participant.vars:
                player.participant.vars['questions_attempted'] = 0
            if 'total_questions_attempted_with_skipped' not in player.participant.vars:
                player.participant.vars['total_questions_attempted_with_skipped'] = 0
            if 'score' not in player.participant.vars:
                player.participant.vars['score'] = C.INITIAL_SCORE

            if not player.participant.vars.get('go_to_results', False):
                if user_answer is None:
                    player.is_answer_correct = False
                    player.is_answer_wrong = False
                    player.participant.vars['skipped_questions_count'] += 1
                else:
                    player.is_answer_correct = (user_answer == correct_answer)
                    player.is_answer_wrong = (user_answer != correct_answer)
                    if player.is_answer_correct:
                        player.participant.vars['correct_answers_count'] += 1
                    else:
                        player.participant.vars['wrong_answers_count'] += 1
                    player.participant.vars['questions_attempted'] += 1

                if player.is_answer_correct:
                    player.participant.vars['score'] += 1
                elif player.is_answer_wrong:
                    player.participant.vars['score'] -= 0.25

                player.participant.vars['total_questions_attempted_with_skipped'] += 1
            else:
                player.is_answer_correct = False
                player.is_answer_wrong = False

            player.correct_answers_count = player.participant.vars['correct_answers_count']
            player.wrong_answers_count = player.participant.vars['wrong_answers_count']
            player.skipped_questions_count = player.participant.vars['skipped_questions_count']
            player.total_questions_attempted_with_skipped = player.participant.vars['total_questions_attempted_with_skipped']
            player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)
            player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)

            questions_attempted = player.participant.vars.get('questions_attempted', 0)
            if questions_attempted > 0:
                total_time_on_questions = 0
                for round_num in range(1, player.round_number + 1):
                    round_time_key = f'question_time_spent_round_{round_num}'
                    round_time = player.participant.vars.get(round_time_key, 0)
                    total_time_on_questions += round_time
                avg_time = total_time_on_questions / questions_attempted
                player.participant.vars['average_time_per_question'] = avg_time
                player.average_time_per_question = avg_time
            else:
                player.participant.vars['average_time_per_question'] = 0
                player.average_time_per_question = 0

            total_questions_with_skipped = player.participant.vars.get('total_questions_attempted_with_skipped', 0)
            if total_questions_with_skipped > 0:
                total_time_on_all_questions = 0
                for round_num in range(1, player.round_number + 1):
                    round_time_key = f'question_time_spent_round_{round_num}'
                    round_time = player.participant.vars.get(round_time_key, 0)
                    total_time_on_all_questions += round_time
                avg_time_with_skipped = total_time_on_all_questions / total_questions_with_skipped
                player.participant.vars['average_time_per_question_with_skipped'] = avg_time_with_skipped
                player.average_time_per_question_with_skipped = avg_time_with_skipped
            else:
                player.participant.vars['average_time_per_question_with_skipped'] = 0
                player.average_time_per_question_with_skipped = 0

            player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
            opponent_score = C.INITIAL_SCORE

            others = player.get_others_in_group()
            if others:
                opponent = others[0]
                opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)
                player.opponent_score = opponent_score

            if player_score > opponent_score:
                player.is_winner = True
                player.competition_result = "Currently leading!"
            elif player_score < opponent_score:
                player.is_winner = False
                player.competition_result = "Currently behind. Keep going!"
            else:
                player.is_winner = False
                player.competition_result = "Currently tied!"

            start_time = player.participant.vars.get('quiz_start_time', time.time())
            elapsed_time = int(time.time() - start_time)
            time_expired = elapsed_time >= C.TOTAL_TIME

            if time_expired and player.round_number < C.NUM_ROUNDS:
                player.participant.vars['go_to_results'] = True

            if player.round_number == C.NUM_ROUNDS or time_expired:
                player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)
                player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)

                quiz_start_time = player.participant.vars.get('quiz_start_time', 0)
                current_time = time.time()
                elapsed_time = current_time - quiz_start_time

                if player.participant.vars.get('go_to_results', False):
                    player.time_jump_occurred = True
                    player.quiz_completion_method = 'time_expired_jump'
                    if player.last_active_timestamp > 0:
                        real_duration = player.last_active_timestamp - quiz_start_time
                        player.time_jump_detection_method = 'last_active_timestamp'
                    else:
                        accumulated_time = sum(
                            player.participant.vars.get(f'question_time_spent_round_{r}', 0)
                            for r in range(1, player.round_number + 1)
                        )
                        real_duration = accumulated_time if accumulated_time > 0 else elapsed_time
                        player.time_jump_detection_method = 'accumulated_round_time'
                else:
                    real_duration = elapsed_time
                    player.quiz_completion_method = 'normal_completion'
                    player.time_jump_detection_method = 'normal_elapsed_time'

                player.total_time_spent = real_duration
                player.real_quiz_duration = real_duration
                player.participant.vars['quiz_end_time'] = current_time
                player.participant.vars['quiz_total_time'] = player.total_time_spent

                if 'competition_results' not in player.participant.vars:
                    player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
                    questions_attempted = player.participant.vars.get('questions_attempted', 0)
                    opponent_score = C.INITIAL_SCORE
                    others = player.get_others_in_group()
                    if others:
                        opponent = others[0]
                        opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)
                        player.opponent_score = opponent_score

                    if player_score > opponent_score:
                        player.is_winner = True
                        result_message = "Congratulations! You won!"
                    elif player_score < opponent_score:
                        player.is_winner = False
                        result_message = "Unfortunately, you lost. Thank you for participating!"
                    else:
                        player.group.handle_tie()
                        return

                    player.competition_result = result_message
                    player.participant.vars['competition_results'] = {
                        'total_questions': C.NUM_ROUNDS,
                        'total_questions_attempted': questions_attempted,
                        'total_questions_attempted_with_skipped': player.participant.vars.get('total_questions_attempted_with_skipped', 0),
                        'player_score': player_score,
                        'opponent_score': opponent_score,
                        'result_message': result_message,
                        'is_winner': player.is_winner,
                        'total_time_spent': player.total_time_spent,
                        'correct_answers_count': player.participant.vars.get('correct_answers_count', 0),
                        'wrong_answers_count': player.participant.vars.get('wrong_answers_count', 0),
                        'skipped_questions_count': player.participant.vars.get('skipped_questions_count', 0),
                        'average_time_per_question': player.participant.vars.get('average_time_per_question', 0),
                        'average_time_per_question_with_skipped': player.participant.vars.get('average_time_per_question_with_skipped', 0)
                    }

        except Exception as e:
            error_msg = f"Error in round {player.round_number}: {str(e)}"
            if not hasattr(player.participant, 'vars'):
                player.participant.vars = {}
            player.participant.vars['quiz_errors'] = player.participant.vars.get('quiz_errors', []) + [error_msg]

            if 'score' in player.participant.vars:
                player.final_score = player.participant.vars['score']
            else:
                player.final_score = C.INITIAL_SCORE

            if 'questions_attempted' in player.participant.vars:
                player.total_questions_attempted = player.participant.vars['questions_attempted']
            else:
                player.total_questions_attempted = 0

            if 'quiz_start_time' in player.participant.vars:
                quiz_start_time = player.participant.vars['quiz_start_time']
                player.total_time_spent = time.time() - quiz_start_time
            else:
                player.total_time_spent = 0

            if 'correct_answers_count' in player.participant.vars:
                player.correct_answers_count = player.participant.vars['correct_answers_count']
            if 'wrong_answers_count' in player.participant.vars:
                player.wrong_answers_count = player.participant.vars['wrong_answers_count']
            if 'skipped_questions_count' in player.participant.vars:
                player.skipped_questions_count = player.participant.vars['skipped_questions_count']
            if 'average_time_per_question' in player.participant.vars:
                player.average_time_per_question = player.participant.vars['average_time_per_question']
            if 'average_time_per_question_with_skipped' in player.participant.vars:
                player.average_time_per_question_with_skipped = player.participant.vars['average_time_per_question_with_skipped']
            if 'total_questions_attempted_with_skipped' in player.participant.vars:
                player.total_questions_attempted_with_skipped = player.participant.vars['total_questions_attempted_with_skipped']

            if not hasattr(player, 'time_jump_detection_method') or not player.time_jump_detection_method:
                player.time_jump_detection_method = 'error_occurred'
            if not hasattr(player, 'quiz_completion_method') or not player.quiz_completion_method:
                player.quiz_completion_method = 'error_occurred'
            if not hasattr(player, 'session_interruption_detected') or player.session_interruption_detected is None:
                player.session_interruption_detected = False
            if not hasattr(player, 'total_interruption_time') or player.total_interruption_time is None:
                player.total_interruption_time = 0
            if not hasattr(player, 'real_quiz_duration') or player.real_quiz_duration is None:
                player.real_quiz_duration = 0
            if not hasattr(player, 'last_active_timestamp') or player.last_active_timestamp is None:
                player.last_active_timestamp = time.time()


page_sequence = [MatchingWaitPage, QuizPage]