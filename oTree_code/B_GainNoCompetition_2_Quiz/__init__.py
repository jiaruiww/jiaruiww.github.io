from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = 'A2_GC_2_Quiz'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 50
    TOTAL_TIME = 240
    INITIAL_SCORE = 0

    WINNING_THRESHOLD = 6

    QUESTION_IMAGES = {
        1: 'Q2cropped.png',
        2: 'Q3cropped.png',
        3: 'Q20cropped.png',
        4: 'Q21cropped.png',
        5: 'Q23cropped.png',
        6: 'Q4cropped.png',
        7: 'Q25cropped.png',
        8: 'Q5cropped.png',
        9: 'Q45cropped.png',
        10: 'Q7cropped.png',
        11: 'Q13cropped.png',
        12: 'Q8cropped.png',
        13: 'Q11cropped.png',
        14: 'Q18cropped.png',
        15: 'Q12cropped.png',
        16: 'Q17cropped.png',
        17: 'Q16cropped.png',
        18: 'Q10cropped.png',
        19: 'Q15cropped.png',
        20: 'Q9cropped.png',
        21: 'Q22cropped.png',
        22: 'Q6cropped.png',
        23: 'Q46cropped.png',
        24: 'Q24cropped.png',
        25: 'Q26cropped.png',
        26: 'Q27cropped.png',
        27: 'Q28cropped.png',
        28: 'Q29cropped.png',
        29: 'Q30cropped.png',
        30: 'Q31cropped.png',
        31: 'Q32cropped.png',
        32: 'Q33cropped.png',
        33: 'Q14cropped.png',
        34: 'Q19cropped.png',
        35: 'Q34cropped.png',
        36: 'Q1cropped.png',
        37: 'Q35cropped.png',
        38: 'Q36cropped.png',
        39: 'Q37cropped.png',
        40: 'Q38cropped.png',
        41: 'Q39cropped.png',
        42: 'Q40cropped.png',
        43: 'Q41cropped.png',
        44: 'Q43cropped.png',
        45: 'Q44cropped.png',
        46: 'Q42cropped.png',
        47: 'Q47cropped.png',
        48: 'Q48cropped.png',
        49: 'Q49cropped.png',
        50: 'Q50cropped.png'
    }

    CHOICE_IMAGES = {
        1: 'Q2cropped_sol.png',
        2: 'Q3cropped_sol.png',
        3: 'Q20cropped_sol.png',
        4: 'Q21cropped_sol.png',
        5: 'Q23cropped_sol.png',
        6: 'Q4cropped_sol.png',
        7: 'Q25cropped_sol.png',
        8: 'Q5cropped_sol.png',
        9: 'Q45cropped_sol.png',
        10: 'Q7cropped_sol.png',
        11: 'Q13cropped_sol.png',
        12: 'Q8cropped_sol.png',
        13: 'Q11cropped_sol.png',
        14: 'Q18cropped_sol.png',
        15: 'Q12cropped_sol.png',
        16: 'Q17cropped_sol.png',
        17: 'Q16cropped_sol.png',
        18: 'Q10cropped_sol.png',
        19: 'Q15cropped_sol.png',
        20: 'Q9cropped_sol.png',
        21: 'Q22cropped_sol.png',
        22: 'Q6cropped_sol.png',
        23: 'Q46cropped_sol.png',
        24: 'Q24cropped_sol.png',
        25: 'Q26cropped_sol.png',
        26: 'Q27cropped_sol.png',
        27: 'Q28cropped_sol.png',
        28: 'Q29cropped_sol.png',
        29: 'Q30cropped_sol.png',
        30: 'Q31cropped_sol.png',
        31: 'Q32cropped_sol.png',
        32: 'Q33cropped_sol.png',
        33: 'Q14cropped_sol.png',
        34: 'Q19cropped_sol.png',
        35: 'Q34cropped_sol.png',
        36: 'Q1cropped_sol.png',
        37: 'Q35cropped_sol.png',
        38: 'Q36cropped_sol.png',
        39: 'Q37cropped_sol.png',
        40: 'Q38cropped_sol.png',
        41: 'Q39cropped_sol.png',
        42: 'Q40cropped_sol.png',
        43: 'Q41cropped_sol.png',
        44: 'Q43cropped_sol.png',
        45: 'Q44cropped_sol.png',
        46: 'Q42cropped_sol.png',
        47: 'Q47cropped_sol.png',
        48: 'Q48cropped_sol.png',
        49: 'Q49cropped_sol.png',
        50: 'Q50cropped_sol.png'
    }

    CORRECT_ANSWERS = {
        1: 2,
        2: 3,
        3: 1,
        4: 3,
        5: 3,
        6: 2,
        7: 4,
        8: 3,
        9: 4,
        10: 1,
        11: 3,
        12: 4,
        13: 1,
        14: 3,
        15: 2,
        16: 1,
        17: 2,
        18: 2,
        19: 1,
        20: 2,
        21: 1,
        22: 2,
        23: 1,
        24: 1,
        25: 1,
        26: 3,
        27: 1,
        28: 4,
        29: 1,
        30: 3,
        31: 1,
        32: 4,
        33: 2,
        34: 1,
        35: 1,
        36: 1,
        37: 4,
        38: 1,
        39: 1,
        40: 4,
        41: 1,
        42: 3,
        43: 2,
        44: 1,
        45: 2,
        46: 1,
        47: 1,
        48: 1,
        49: 2,
        50: 1
    }

    CORRECT_SCORE = 1.0
    WRONG_SCORE = -0.25
    SKIP_SCORE = 0.0


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    prolific_id = models.StringField(default="", blank=True)

    user_answer = models.IntegerField(
        label="Your Answer",
        choices=[
            [1, 'A'],
            [2, 'B'],
            [3, 'C'],
            [4, 'D'],
        ],
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

    competition_result = models.StringField(blank=True)

    correct_answers_count = models.IntegerField(initial=0)
    wrong_answers_count = models.IntegerField(initial=0)
    skipped_questions_count = models.IntegerField(initial=0)

    results_message = models.StringField(blank=True)

    total_questions_attempted_with_skipped = models.IntegerField(initial=0)

    average_time_per_question = models.FloatField(initial=0)
    average_time_per_question_with_skipped = models.FloatField(initial=0)


class QuizPage(Page):
    form_model = 'player'
    form_fields = ['user_answer']

    timeout_submission = {'user_answer': None}

    @staticmethod
    def before_session_starts(subsession):
        for player in subsession.get_players():
            player.participant.vars['score'] = C.INITIAL_SCORE
            player.participant.vars['quiz_start_time'] = time.time()
            player.participant.vars['questions_attempted'] = 0

            if 'prolific_id' in player.participant.vars:
                player.prolific_id = player.participant.vars['prolific_id']
            elif player.participant.label:
                player.prolific_id = player.participant.label

    @staticmethod
    def live_method(player: Player, data):
        player_score = player.participant.vars.get('score', C.INITIAL_SCORE)

        start_time = player.participant.vars.get('quiz_start_time', time.time())
        current_time = time.time()
        elapsed_time = int(current_time - start_time)
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)

        player.participant.vars['last_connection_time'] = current_time

        is_reconnect = data.get('reconnecting', False)
        if is_reconnect:
            reconnect_events = player.participant.vars.get('reconnect_events', [])
            reconnect_events.append({
                'round': player.round_number,
                'time': current_time,
                'elapsed_time': elapsed_time
            })
            player.participant.vars['reconnect_events'] = reconnect_events

        response = {
            'player_score': player_score,
            'remaining_time': remaining_time,
            'server_time': current_time
        }

        client_time = data.get('clientTime', None)
        if client_time:
            response['client_time'] = client_time

        if remaining_time <= 0 and player.round_number < C.NUM_ROUNDS:
            response['time_expired'] = True

        return {player.id_in_group: response}

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
        if player.round_number == 1:
            if 'score' not in player.participant.vars:
                player.participant.vars['score'] = C.INITIAL_SCORE
                player.participant.vars['quiz_start_time'] = time.time()
                player.participant.vars['questions_attempted'] = 0

                player.participant.vars['correct_answers_count'] = 0
                player.participant.vars['wrong_answers_count'] = 0
                player.participant.vars['skipped_questions_count'] = 0

                if 'prolific_id' in player.participant.vars:
                    player.prolific_id = player.participant.vars['prolific_id']
                elif player.participant.label:
                    player.prolific_id = player.participant.label

        if player.round_number > 1:
            player_in_round_1 = player.in_round(1)
            player.prolific_id = player_in_round_1.prolific_id

        question_image = C.QUESTION_IMAGES.get(player.round_number, "")
        choice_image = C.CHOICE_IMAGES.get(player.round_number, "")
        score = player.participant.vars.get('score', C.INITIAL_SCORE)

        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)

        player.participant.vars['page_start_time'] = time.time()

        return {
            'question_number': player.round_number,
            'question_image': question_image,
            'choice_image': choice_image,
            'score': score,
            'remaining_time': remaining_time,
            'total_time': C.TOTAL_TIME,
            'initial_score': C.INITIAL_SCORE,
            'winning_threshold': C.WINNING_THRESHOLD
        }

    @staticmethod
    def is_displayed(player: Player):
        if player.participant.vars.get('go_to_results', False):
            return False

        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        time_expired = elapsed_time >= C.TOTAL_TIME

        if time_expired and player.round_number > 1:
            player.participant.vars['go_to_results'] = True

            player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)
            player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)

            player.correct_answers_count = player.participant.vars.get('correct_answers_count', 0)
            player.wrong_answers_count = player.participant.vars.get('wrong_answers_count', 0)
            player.skipped_questions_count = player.participant.vars.get('skipped_questions_count', 0)

            is_winner = player.final_score >= C.WINNING_THRESHOLD
            player.is_winner = is_winner

            if is_winner:
                player.competition_result = "Won by exceeding threshold"
            else:
                player.competition_result = "Did not exceed threshold"

            return False

        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        try:
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

                if 'questions_attempted' not in player.participant.vars:
                    player.participant.vars['questions_attempted'] = 0
                player.participant.vars['questions_attempted'] += 1

            if 'score' not in player.participant.vars:
                player.participant.vars['score'] = C.INITIAL_SCORE

            if user_answer is None:
                pass
            elif player.is_answer_correct:
                player.participant.vars['score'] += C.CORRECT_SCORE
            else:
                player.participant.vars['score'] += C.WRONG_SCORE

            if 'total_questions_attempted_with_skipped' not in player.participant.vars:
                player.participant.vars['total_questions_attempted_with_skipped'] = 0
            player.participant.vars['total_questions_attempted_with_skipped'] += 1

            player.correct_answers_count = player.participant.vars['correct_answers_count']
            player.wrong_answers_count = player.participant.vars['wrong_answers_count']
            player.skipped_questions_count = player.participant.vars['skipped_questions_count']
            player.total_questions_attempted_with_skipped = player.participant.vars[
                'total_questions_attempted_with_skipped']

            player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)

            quiz_start_time = player.participant.vars.get('quiz_start_time', time.time())
            current_total_time = time.time() - quiz_start_time
            player.total_time_spent = current_total_time
            player.participant.vars['quiz_total_time'] = current_total_time

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

            player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)

            current_score = player.participant.vars.get('score', C.INITIAL_SCORE)
            player.is_winner = (current_score >= C.WINNING_THRESHOLD)

            if player.is_winner:
                player.competition_result = "Won by exceeding threshold"
                player.results_message = f"Congratulations! You scored {C.WINNING_THRESHOLD} or above."
            else:
                player.competition_result = "Did not exceed threshold"
                player.results_message = f"Currently below {C.WINNING_THRESHOLD}. Keep going!"

            start_time = player.participant.vars.get('quiz_start_time', time.time())
            elapsed_time = int(time.time() - start_time)
            time_expired = elapsed_time >= C.TOTAL_TIME

            if time_expired and player.round_number < C.NUM_ROUNDS:
                player.participant.vars['go_to_results'] = True

            if player.round_number == C.NUM_ROUNDS or time_expired:
                quiz_start_time = player.participant.vars.get('quiz_start_time', 0)
                quiz_end_time = time.time()
                player.total_time_spent = quiz_end_time - quiz_start_time

                player.participant.vars['quiz_end_time'] = quiz_end_time
                player.participant.vars['quiz_total_time'] = player.total_time_spent

                if 'competition_results' not in player.participant.vars:
                    player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
                    questions_attempted = player.participant.vars.get('questions_attempted', 0)

                    correct_answers_count = player.participant.vars.get('correct_answers_count', 0)
                    wrong_answers_count = player.participant.vars.get('wrong_answers_count', 0)
                    skipped_questions_count = player.participant.vars.get('skipped_questions_count', 0)

                    if player_score >= C.WINNING_THRESHOLD:
                        player.is_winner = True
                        result_message = f"Congratulations! You scored {C.WINNING_THRESHOLD} or above."
                        competition_result = "Won by exceeding threshold"
                    else:
                        player.is_winner = False
                        result_message = f"Unfortunately, you scored below {C.WINNING_THRESHOLD}. Thank you for participating!"
                        competition_result = "Did not exceed threshold"

                    player.competition_result = competition_result
                    player.results_message = result_message

                    player.participant.vars['results_message'] = result_message
                    player.participant.vars['competition_result'] = competition_result

                    player.participant.vars['quiz_end_time'] = time.time()

                    player.participant.vars['competition_results'] = {
                        'total_questions': C.NUM_ROUNDS,
                        'total_questions_attempted': questions_attempted,
                        'total_questions_attempted_with_skipped': player.participant.vars.get(
                            'total_questions_attempted_with_skipped', 0),
                        'player_score': player_score,
                        'winning_threshold': C.WINNING_THRESHOLD,
                        'is_winner': player.is_winner,
                        'total_time_spent': player.total_time_spent,
                        'correct_answers_count': correct_answers_count,
                        'wrong_answers_count': wrong_answers_count,
                        'skipped_questions_count': skipped_questions_count,
                        'average_time_per_question': player.participant.vars.get('average_time_per_question', 0),
                        'average_time_per_question_with_skipped': player.participant.vars.get(
                            'average_time_per_question_with_skipped', 0)
                    }

        except Exception as e:
            error_msg = f"Error in round {player.round_number}: {str(e)}"
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
                player.average_time_per_question_with_skipped = player.participant.vars[
                    'average_time_per_question_with_skipped']
            if 'total_questions_attempted_with_skipped' in player.participant.vars:
                player.total_questions_attempted_with_skipped = player.participant.vars[
                    'total_questions_attempted_with_skipped']


page_sequence = [QuizPage]