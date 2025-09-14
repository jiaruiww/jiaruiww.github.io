from otree.api import *
import random
import time


class C(BaseConstants):
    NAME_IN_URL = 'A1_GT_2_Quiz'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 50
    TOTAL_TIME = 240
    INITIAL_SCORE = 0  # Changed to start at 0 instead of 50

    RETURN_CODE = 'C1FIVYUV'  # Code for pairing timeout returns

    # Question image mapping rearranged according to the latest Excel file order
    QUESTION_IMAGES = {
        1: 'Q2cropped.png',  # Q2 -> Position 1
        2: 'Q3cropped.png',  # Q3 -> Position 2
        3: 'Q20cropped.png',  # Q20 -> Position 3
        4: 'Q21cropped.png',  # Q21 -> Position 4
        5: 'Q23cropped.png',  # Q23 -> Position 5
        6: 'Q4cropped.png',  # Q4 -> Position 6
        7: 'Q25cropped.png',  # Q25 -> Position 7
        8: 'Q5cropped.png',  # Q5 -> Position 8
        9: 'Q45cropped.png',  # Q45 -> Position 9
        10: 'Q7cropped.png',  # Q7 -> Position 10
        11: 'Q13cropped.png',  # Q13 -> Position 11
        12: 'Q8cropped.png',  # Q8 -> Position 12
        13: 'Q11cropped.png',  # Q11 -> Position 13
        14: 'Q18cropped.png',  # Q18 -> Position 14
        15: 'Q12cropped.png',  # Q12 -> Position 15
        16: 'Q17cropped.png',  # Q17 -> Position 16
        17: 'Q16cropped.png',  # Q16 -> Position 17
        18: 'Q10cropped.png',  # Q10 -> Position 18
        19: 'Q15cropped.png',  # Q15 -> Position 19
        20: 'Q9cropped.png',  # Q9 -> Position 20
        21: 'Q22cropped.png',  # Q22 -> Position 21
        22: 'Q6cropped.png',  # Q6 -> Position 22
        23: 'Q46cropped.png',  # Q46 -> Position 23
        24: 'Q24cropped.png',  # Q24 -> Position 24
        25: 'Q26cropped.png',  # Q26 -> Position 25
        26: 'Q27cropped.png',  # Q27 -> Position 26
        27: 'Q28cropped.png',  # Q28 -> Position 27
        28: 'Q29cropped.png',  # Q29 -> Position 28
        29: 'Q30cropped.png',  # Q30 -> Position 29
        30: 'Q31cropped.png',  # Q31 -> Position 30
        31: 'Q32cropped.png',  # Q32 -> Position 31
        32: 'Q33cropped.png',  # Q33 -> Position 32
        33: 'Q14cropped.png',  # Q14 -> Position 33
        34: 'Q19cropped.png',  # Q19 -> Position 34
        35: 'Q34cropped.png',  # Q34 -> Position 35
        36: 'Q1cropped.png',  # Q1 -> Position 36
        37: 'Q35cropped.png',  # Q35 -> Position 37
        38: 'Q36cropped.png',  # Q36 -> Position 38
        39: 'Q37cropped.png',  # Q37 -> Position 39
        40: 'Q38cropped.png',  # Q38 -> Position 40
        41: 'Q39cropped.png',  # Q39 -> Position 41
        42: 'Q40cropped.png',  # Q40 -> Position 42
        43: 'Q41cropped.png',  # Q41 -> Position 43
        44: 'Q43cropped.png',  # Q43 -> Position 44
        45: 'Q44cropped.png',  # Q44 -> Position 45
        46: 'Q42cropped.png',  # Q42 -> Position 46
        47: 'Q47cropped.png',  # Q47 -> Position 47
        48: 'Q48cropped.png',  # Q48 -> Position 48
        49: 'Q49cropped.png',  # Q49 -> Position 49
        50: 'Q50cropped.png'  # Q50 -> Position 50
    }

    # Choice image mapping rearranged according to the latest Excel file order
    CHOICE_IMAGES = {
        1: 'Q2cropped_sol.png',  # Q2 -> Position 1
        2: 'Q3cropped_sol.png',  # Q3 -> Position 2
        3: 'Q20cropped_sol.png',  # Q20 -> Position 3
        4: 'Q21cropped_sol.png',  # Q21 -> Position 4
        5: 'Q23cropped_sol.png',  # Q23 -> Position 5
        6: 'Q4cropped_sol.png',  # Q4 -> Position 6
        7: 'Q25cropped_sol.png',  # Q25 -> Position 7
        8: 'Q5cropped_sol.png',  # Q5 -> Position 8
        9: 'Q45cropped_sol.png',  # Q45 -> Position 9
        10: 'Q7cropped_sol.png',  # Q7 -> Position 10
        11: 'Q13cropped_sol.png',  # Q13 -> Position 11
        12: 'Q8cropped_sol.png',  # Q8 -> Position 12
        13: 'Q11cropped_sol.png',  # Q11 -> Position 13
        14: 'Q18cropped_sol.png',  # Q18 -> Position 14
        15: 'Q12cropped_sol.png',  # Q12 -> Position 15
        16: 'Q17cropped_sol.png',  # Q17 -> Position 16
        17: 'Q16cropped_sol.png',  # Q16 -> Position 17
        18: 'Q10cropped_sol.png',  # Q10 -> Position 18
        19: 'Q15cropped_sol.png',  # Q15 -> Position 19
        20: 'Q9cropped_sol.png',  # Q9 -> Position 20
        21: 'Q22cropped_sol.png',  # Q22 -> Position 21
        22: 'Q6cropped_sol.png',  # Q6 -> Position 22
        23: 'Q46cropped_sol.png',  # Q46 -> Position 23
        24: 'Q24cropped_sol.png',  # Q24 -> Position 24
        25: 'Q26cropped_sol.png',  # Q26 -> Position 25
        26: 'Q27cropped_sol.png',  # Q27 -> Position 26
        27: 'Q28cropped_sol.png',  # Q28 -> Position 27
        28: 'Q29cropped_sol.png',  # Q29 -> Position 28
        29: 'Q30cropped_sol.png',  # Q30 -> Position 29
        30: 'Q31cropped_sol.png',  # Q31 -> Position 30
        31: 'Q32cropped_sol.png',  # Q32 -> Position 31
        32: 'Q33cropped_sol.png',  # Q33 -> Position 32
        33: 'Q14cropped_sol.png',  # Q14 -> Position 33
        34: 'Q19cropped_sol.png',  # Q19 -> Position 34
        35: 'Q34cropped_sol.png',  # Q34 -> Position 35
        36: 'Q1cropped_sol.png',  # Q1 -> Position 36
        37: 'Q35cropped_sol.png',  # Q35 -> Position 37
        38: 'Q36cropped_sol.png',  # Q36 -> Position 38
        39: 'Q37cropped_sol.png',  # Q37 -> Position 39
        40: 'Q38cropped_sol.png',  # Q38 -> Position 40
        41: 'Q39cropped_sol.png',  # Q39 -> Position 41
        42: 'Q40cropped_sol.png',  # Q40 -> Position 42
        43: 'Q41cropped_sol.png',  # Q41 -> Position 43
        44: 'Q43cropped_sol.png',  # Q43 -> Position 44
        45: 'Q44cropped_sol.png',  # Q44 -> Position 45
        46: 'Q42cropped_sol.png',  # Q42 -> Position 46
        47: 'Q47cropped_sol.png',  # Q47 -> Position 47
        48: 'Q48cropped_sol.png',  # Q48 -> Position 48
        49: 'Q49cropped_sol.png',  # Q49 -> Position 49
        50: 'Q50cropped_sol.png'  # Q50 -> Position 50
    }

    # Correct answers rearranged according to the latest Excel file order
    CORRECT_ANSWERS = {
        1: 2,  # B - Q2's answer
        2: 3,  # C - Q3's answer
        3: 1,  # A - Q20's answer
        4: 3,  # C - Q21's answer
        5: 3,  # C - Q23's answer
        6: 2,  # B - Q4's answer
        7: 4,  # D - Q25's answer
        8: 3,  # C - Q5's answer
        9: 4,  # D - Q45's answer
        10: 1,  # A - Q7's answer
        11: 3,  # C - Q13's answer
        12: 4,  # D - Q8's answer
        13: 1,  # A - Q11's answer
        14: 3,  # C - Q18's answer
        15: 2,  # B - Q12's answer
        16: 1,  # A - Q17's answer
        17: 2,  # B - Q16's answer
        18: 2,  # B - Q10's answer
        19: 1,  # A - Q15's answer
        20: 2,  # B - Q9's answer
        21: 1,  # A - Q22's answer
        22: 2,  # B - Q6's answer
        23: 1,  # A - Q46's answer
        24: 1,  # A - Q24's answer
        25: 1,  # A - Q26's answer
        26: 3,  # C - Q27's answer
        27: 1,  # A - Q28's answer
        28: 4,  # D - Q29's answer
        29: 1,  # A - Q30's answer
        30: 3,  # C - Q31's answer
        31: 1,  # A - Q32's answer
        32: 4,  # D - Q33's answer
        33: 2,  # B - Q14's answer
        34: 1,  # A - Q19's answer
        35: 1,  # A - Q34's answer
        36: 1,  # A - Q1's answer
        37: 4,  # D - Q35's answer
        38: 1,  # A - Q36's answer
        39: 1,  # A - Q37's answer
        40: 4,  # D - Q38's answer
        41: 1,  # A - Q39's answer
        42: 3,  # C - Q40's answer
        43: 2,  # B - Q41's answer
        44: 1,  # A - Q43's answer
        45: 2,  # B - Q44's answer
        46: 1,  # A - Q42's answer
        47: 1,  # A - Q47's answer
        48: 1,  # A - Q48's answer
        49: 2,  # B - Q49's answer
        50: 1  # A - Q50's answer
    }


class Subsession(BaseSubsession):
    def creating_session(self):
        # Only handle grouping for rounds after round 1
        # Round 1 grouping is handled by MatchingWaitPage
        if self.round_number > 1:
            self.group_like_round(1)


class Group(BaseGroup):
    quiz_start_timestamp = models.FloatField(initial=0)
    both_players_ready = models.BooleanField(initial=False)

    def handle_tie(self):
        """Handle tie situations, ensuring one player is the winner and one is the loser"""
        players = self.get_players()
        if len(players) != 2:
            return  # If there are not two players, do not execute

        p1, p2 = players

        # Randomly select a player as the winner
        # Use p1.id_in_group as random seed to ensure deterministic results
        random.seed(p1.id_in_group)
        winner_idx = random.randint(0, 1)

        if winner_idx == 0:
            # p1 is the winner
            p1.is_winner = True
            p1.tie_occurred = True
            p1.tie_random_result = "Won by random selection"
            p1.competition_result = "It's a tie. You are randomly selected as the top performer."

            p2.is_winner = False
            p2.tie_occurred = True
            p2.tie_random_result = "Lost by random selection"
            p2.competition_result = "It's a tie. You are randomly selected as the bottom performer."
        else:
            # p2 is the winner
            p1.is_winner = False
            p1.tie_occurred = True
            p1.tie_random_result = "Lost by random selection"
            p1.competition_result = "It's a tie. You are randomly selected as the bottom performer."

            p2.is_winner = True
            p2.tie_occurred = True
            p2.tie_random_result = "Won by random selection"
            p2.competition_result = "It's a tie. You are randomly selected as the top performer."

        # Update participant variables
        for p in players:
            opponent = p.get_others_in_group()[0]
            p.participant.vars['competition_results'] = {
                'total_questions': C.NUM_ROUNDS,
                'total_questions_attempted': p.participant.vars.get('questions_attempted', 0),
                'total_questions_attempted_with_skipped': p.participant.vars.get(
                    'total_questions_attempted_with_skipped', 0),
                'player_score': p.participant.vars.get('score', C.INITIAL_SCORE),
                'opponent_score': opponent.participant.vars.get('score', C.INITIAL_SCORE),
                'result_message': p.competition_result,
                'is_winner': p.is_winner,
                'total_time_spent': p.total_time_spent,
                'average_time_per_question': p.participant.vars.get('average_time_per_question', 0),
                'average_time_per_question_with_skipped': p.participant.vars.get(
                    'average_time_per_question_with_skipped', 0)  # Add this line
            }


class Player(BasePlayer):
    # Add Prolific ID field for data connection
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

    # Data collection fields
    is_answer_correct = models.BooleanField(initial=False)  # Whether the answer is correct
    is_answer_wrong = models.BooleanField(initial=False)  # Whether the answer is wrong (not skipped)
    question_time_spent = models.FloatField(initial=0)  # Time spent on each page
    final_score = models.FloatField(initial=C.INITIAL_SCORE)  # Final score, initialized with 0
    is_winner = models.BooleanField(initial=False)  # Whether the player is the winner
    total_questions_attempted = models.IntegerField(initial=0)  # Total questions attempted
    total_time_spent = models.FloatField(initial=0)  # Total time spent on quiz
    # In Player class (around line 297), add:
    correct_answers_count = models.IntegerField(initial=0)
    # In Player class, add this line after the correct_answers_count field:
    wrong_answers_count = models.IntegerField(initial=0)
    # Add this line in Player class after the wrong_answers_count field
    skipped_questions_count = models.IntegerField(initial=0)

    # Pairing related fields
    paired_partner_id = models.StringField(blank=True)  # Partner's participant.id
    paired_partner_prolific_id = models.StringField(blank=True)  # Partner's prolific_id
    is_successfully_paired = models.BooleanField(initial=False)  # Whether successfully paired
    matching_wait_time = models.FloatField(blank=True, null=True)  # Matching wait time (seconds)
    matching_timeout_occurred = models.BooleanField(initial=False)  # Whether matching timeout occurred

    # Group competition related
    competition_result = models.StringField(blank=True)  # Competition result description
    opponent_score = models.FloatField(blank=True, null=True)  # Opponent's score
    tie_occurred = models.BooleanField(initial=False)  # Whether a tie occurred
    tie_random_result = models.StringField(blank=True)  # Tie random result description

    total_questions_attempted_with_skipped = models.IntegerField(initial=0)

    # In the Player class (around line 276)
    average_time_per_question = models.FloatField(initial=0)

    # Add this new field in the Player class after the average_time_per_question field
    average_time_per_question_with_skipped = models.FloatField(initial=0)

    time_jump_occurred = models.BooleanField(initial=False)
    time_jump_detection_method = models.StringField(blank=True)
    real_quiz_duration = models.FloatField(initial=0)
    last_active_timestamp = models.FloatField(initial=0)
    session_interruption_detected = models.BooleanField(initial=False)
    total_interruption_time = models.FloatField(initial=0)
    quiz_completion_method = models.StringField(blank=True)



def group_by_arrival_time_method(subsession, waiting_players):
    # Check if waiting_players is a Subsession object
    if hasattr(waiting_players, 'get_players'):
        # If it's a Subsession, get the players
        players_to_check = waiting_players.get_players()
    else:
        # Otherwise assume it's already a list of players
        players_to_check = waiting_players

    # Now filter out timed out players
    active_players = []
    for p in players_to_check:
        if not p.participant.vars.get('matching_timed_out', False):
            active_players.append(p)

    # Only form a group if we have at least 2 active players
    if len(active_players) >= 2:
        # Take the first two players who haven't timed out
        return active_players[:2]

    # Not enough active players, don't form a group yet
    return None


class MatchingWaitPage(WaitPage):
    group_by_arrival_time = True
    template_name = 'A1_GT_2_Quiz/MatchingWaitPage.html'  # Use your custom template

    @staticmethod
    def js_vars(player: Player):
        # Set timeout to 10 seconds
        current_time = time.time()
        start_time = player.participant.vars.get('wait_page_start_time', current_time)
        elapsed_time = current_time - start_time
        timeout_duration = 300  # 10 seconds
        remaining_time = max(0, timeout_duration - elapsed_time)

        # Add synchronization status check
        if player.group and player.group.both_players_ready:
            return {
                'timeout': remaining_time,
                'both_ready': True,  # New flag
                'redirect_to_quiz': True  # Notify frontend to redirect
            }
        return {'timeout': remaining_time}


    @staticmethod
    def vars_for_template(player: Player):
        # Check if timeout has occurred
        current_time = time.time()
        start_time = player.participant.vars.get('wait_page_start_time', current_time)
        elapsed_time = current_time - start_time
        timeout_duration = 300  # 10 seconds
        timeout_happened = elapsed_time >= timeout_duration

        # If timeout occurred, mark player as timed out in participant vars
        # This is crucial for the get_players_for_group method
        if timeout_happened:
            player.participant.vars['matching_timed_out'] = True
            # Also mark the player as having seen the timeout message
            player.participant.vars['timeout_message_shown'] = True

            # Persist timeout status to Player model
            player.is_successfully_paired = False
            player.matching_timeout_occurred = True
            player.matching_wait_time = elapsed_time
            player.competition_result = "Not paired due to timeout"

        # Check synchronization status
        is_synced = False
        redirect_url = ''
        if player.group and player.group.both_players_ready:
            is_synced = True
            redirect_url = f'/p/{player.participant.code}/A1_GT_2_Quiz/QuizPage/1/'

        return {
            'timeout_happened': timeout_happened,
            'return_code': C.RETURN_CODE,
            'is_synced': is_synced,  # Add this line
            'redirect_url': redirect_url  # Add this line
        }

    @staticmethod
    def is_displayed(player: Player):
        # Set the start time on first visit
        if 'wait_page_start_time' not in player.participant.vars:
            player.participant.vars['wait_page_start_time'] = time.time()

        # Check if this player has already timed out
        if player.participant.vars.get('matching_timed_out', False):
            return True  # Changed from False to True to keep them on this page

        return player.round_number == 1

    @staticmethod
    def after_all_players_arrive(group: Group):
        # Initialize player variables once group is formed
        players = group.get_players()
        if len(players) == 2:
            p1, p2 = players
            # Use participant.id instead of id_in_session
            p1.participant.vars['paired_partner_id'] = p2.participant.id
            p2.participant.vars['paired_partner_id'] = p1.participant.id

            # Persist to Player model
            p1.paired_partner_id = str(p2.participant.id)
            p2.paired_partner_id = str(p1.participant.id)

            # Record successful pairing status
            p1.is_successfully_paired = True
            p2.is_successfully_paired = True

            # Record prolific_id cross-association
            p1.paired_partner_prolific_id = p2.prolific_id
            p2.paired_partner_prolific_id = p1.prolific_id

            # Record matching wait time
            if 'wait_page_start_time' in p1.participant.vars:
                p1.matching_wait_time = time.time() - p1.participant.vars['wait_page_start_time']
            if 'wait_page_start_time' in p2.participant.vars:
                p2.matching_wait_time = time.time() - p2.participant.vars['wait_page_start_time']

            # Mark that both players in the group are ready
            group.both_players_ready = True


        # Initialize scores and timestamps for all players
        for p in players:
            # Get prolific_id from participant.vars
            # Get prolific_id from participant.vars (three-layer safeguard mechanism)
            if 'prolific_id' in p.participant.vars:
                # First layer: Get previously stored ID from participant.vars
                p.prolific_id = p.participant.vars['prolific_id']
            elif p.participant.label:
                # Second layer: Use participant.label (usually auto-filled by URL parameters)
                p.prolific_id = p.participant.label
            else:
                # Third layer: Generate a unique identifier based on session and player ID
                # Format: session_{session_id}_player_{id_in_group}_{random_string}
                import random
                import string
                random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
                fallback_id = f"session_{p.session.id}_player_{p.id_in_group}_{random_suffix}"
                p.prolific_id = fallback_id

                # Log this exception for subsequent analysis
                print(f"Warning: Participant {p.id_in_group} in session {p.session.id} is missing prolific_id, using generated ID: {fallback_id}")

                # Optional: Store this generated ID in participant.vars for use in subsequent apps
                p.participant.vars['prolific_id'] = fallback_id

            p.participant.vars['score'] = C.INITIAL_SCORE  # Initialize with 0 points
            p.participant.vars['quiz_start_time'] = time.time()
            p.participant.vars['questions_attempted'] = 0  # Initialize questions attempted counter


class QuizPage(Page):
    form_model = 'player'
    form_fields = ['user_answer']

    # Define timeout_submission to handle automatic skipping
    timeout_submission = {'user_answer': None}

    @staticmethod
    def live_method(player: Player, data):
        """
        Enhanced live_method for production robustness - Enhanced real-time method for improved production environment stability
        """
        try:
            # 1. Validate basic data integrity
            if not hasattr(player, 'participant') or not player.participant:
                return {player.id_in_group: {'error': 'Invalid player data'}}

            if not hasattr(player, 'group') or not player.group:
                return {player.id_in_group: {'error': 'No group assigned'}}

            # 2. Safely get player score
            player_score = player.participant.vars.get('score', C.INITIAL_SCORE)

            # 3. Safely get opponent information
            opponent_score = C.INITIAL_SCORE
            opponent_correct_count = 0

            try:
                others = player.get_others_in_group()
                if others and len(others) > 0:
                    opponent = others[0]
                    if opponent and hasattr(opponent, 'participant') and opponent.participant:
                        # Use get() method to avoid KeyError
                        opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)
                        opponent_correct_count = opponent.participant.vars.get('correct_answers_count', 0)
            except (AttributeError, IndexError, TypeError) as e:
                # Log error but don't interrupt execution
                print(f"Warning: Error getting opponent data for player {player.id_in_group}: {e}")

            # 4. Safe time calculation
            try:
                start_time = player.participant.vars.get('quiz_start_time')
                if start_time is None:
                    # If no start time, use current time and log
                    start_time = time.time()
                    player.participant.vars['quiz_start_time'] = start_time
                    print(f"Warning: Missing quiz_start_time for player {player.id_in_group}, using current time")

                elapsed_time = int(time.time() - start_time)
                remaining_time = max(0, C.TOTAL_TIME - elapsed_time)

            except (TypeError, ValueError) as e:
                # Fallback for time calculation errors
                print(f"Error calculating time for player {player.id_in_group}: {e}")
                remaining_time = C.TOTAL_TIME

            # 5. Check time expiry logic (maintain original logic)
            time_expired = False
            if remaining_time <= 0 and player.round_number < C.NUM_ROUNDS:
                time_expired = True

            # 6. Data validation and boundary checks
            player_score = max(-50, min(100, float(player_score)))  # Limit score range
            opponent_score = max(-50, min(100, float(opponent_score)))  # Limit score range
            opponent_correct_count = max(0, min(C.NUM_ROUNDS, int(opponent_correct_count)))  # Limit correct answer count
            remaining_time = max(0, min(C.TOTAL_TIME, int(remaining_time)))  # Limit time range

            # 7. Build return data (ensure all fields have valid values, maintain original field names)
            response_data = {
                'player_score': player_score,
                'teammate_score': opponent_score,  # Maintain original field name
                'teammate_correct_count': opponent_correct_count,  # Maintain original field name
                'remaining_time': remaining_time
            }

            # 8. If time expired, add time expiry signal (maintain original logic)
            if time_expired:
                response_data['time_expired'] = True

            return {player.id_in_group: response_data}

        except Exception as e:
            # 9. Global exception handling - never let live_method crash
            error_msg = f"Critical error in live_method for player {getattr(player, 'id_in_group', 'unknown')}: {str(e)}"
            print(error_msg)

            # Return minimal usable dataset (maintain original field names and default values)
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
        # Get the initial start time from participant.vars
        start_time = player.participant.vars.get('quiz_start_time')
        # If there's no start time, set the current time (this generally only happens in rare cases)
        if start_time is None:
            start_time = time.time()
            player.participant.vars['quiz_start_time'] = start_time
        # Calculate elapsed seconds
        elapsed_time = int(time.time() - start_time)
        # Remaining time = total time - elapsed time, ensure it's not negative
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)
        return remaining_time

    @staticmethod
    def vars_for_template(player: Player):
        # Ensure prolific_id is set (even in subsequent rounds)
        if player.round_number > 1:
            player_in_round_1 = player.in_round(1)
            player.prolific_id = player_in_round_1.prolific_id

        # Get question image
        question_image = C.QUESTION_IMAGES.get(player.round_number, "")
        choice_image = C.CHOICE_IMAGES.get(player.round_number, "")

        # Get current player score
        score = player.participant.vars.get('score', C.INITIAL_SCORE)

        # Get teammate information
        others = player.get_others_in_group()
        if others:
            teammate_score = others[0].participant.vars.get('score', C.INITIAL_SCORE)
            teammate_correct_count = others[0].participant.vars.get('correct_answers_count', 0)
        else:
            teammate_score = C.INITIAL_SCORE
            teammate_correct_count = 0

        # Fix: Ensure all values are not None, provide safe default values
        teammate_correct_count = teammate_correct_count if teammate_correct_count is not None else 0
        teammate_score = teammate_score if teammate_score is not None else C.INITIAL_SCORE

        # New: Key: Calculate progress bar width percentage (ensure always returns valid integer)
        max_display_score = 25
        if teammate_correct_count > max_display_score:
            teammate_bar_width = 100
        else:
            # Ensure calculation result is a valid integer
            teammate_bar_width = max(0, int((teammate_correct_count / max_display_score) * 100))

        # Fix: Calculate remaining time
        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        remaining_time = max(0, C.TOTAL_TIME - elapsed_time)

        # Record page start time for calculating time spent
        player.participant.vars['page_start_time'] = time.time()

        return {
            'question_number': player.round_number,
            'question_image': question_image,
            'choice_image': choice_image,
            'score': score,
            'teammate_score': teammate_score,
            'teammate_correct_count': teammate_correct_count,  # Ensure not None
            'teammate_bar_width': teammate_bar_width,  # Ensure valid integer
            'remaining_time': remaining_time,
            'total_time': C.TOTAL_TIME,
            'initial_score': C.INITIAL_SCORE
        }


    @staticmethod
    def is_displayed(player: Player):
        # Skip all remaining rounds if time is up
        if player.participant.vars.get('go_to_results', False):
            return False

        # NEW: Skip the QuizPage entirely if player timed out during matching
        if player.participant.vars.get('matching_timed_out', False):
            return False

        # Track the last displayed round
        player.participant.vars['last_displayed_round'] = player.round_number

        # Key modification: Set synchronized quiz start time on first visit
        if player.round_number == 1 and 'quiz_start_time' not in player.participant.vars:
             # Ensure group information exists
             if player.group:
                # If quiz_start_timestamp is not yet set, set it
                 if player.group.quiz_start_timestamp == 0:
                     player.group.quiz_start_timestamp = time.time()

                 # Use the group's synchronized timestamp as each player's quiz start time
                 player.participant.vars['quiz_start_time'] = player.group.quiz_start_timestamp

        # Check if time is up
        start_time = player.participant.vars.get('quiz_start_time', time.time())
        elapsed_time = int(time.time() - start_time)
        time_expired = elapsed_time >= C.TOTAL_TIME

        # If time expired and not on the first question, skip to results
        if time_expired and player.round_number > 1:
            player.participant.vars['go_to_results'] = True
            return False

        return True

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Add data saving mechanism for abnormal exits
        try:
            current_time = time.time()

            # ==========================================================================
            # New feature: Update variables every round (consistent with A2/A4)
            # ==========================================================================

            # 1. Time-related variables - updated every round
            quiz_start_time = player.participant.vars.get('quiz_start_time', current_time)

            # total_time_spent = current accumulated time (apparent elapsed time)
            elapsed_time = current_time - quiz_start_time
            player.total_time_spent = elapsed_time

            # last_active_timestamp = current timestamp
            player.last_active_timestamp = current_time

            # real_quiz_duration = current actual time spent (net answering time excluding interruptions)
            accumulated_round_time = 0
            for round_num in range(1, player.round_number + 1):
                round_time_key = f'question_time_spent_round_{round_num}'
                round_time = player.participant.vars.get(round_time_key, 0)
                accumulated_round_time += round_time

            # If interruption detected, use accumulated time; otherwise use elapsed time
            if hasattr(player, 'session_interruption_detected') and player.session_interruption_detected:
                player.real_quiz_duration = accumulated_round_time
            else:
                player.real_quiz_duration = elapsed_time

            # 2. Detection status variables - updated every round, providing current best estimate
            if hasattr(player, 'session_interruption_detected') and player.session_interruption_detected:
                player.time_jump_detection_method = 'accumulated_round_time'
            elif player.last_active_timestamp > 0:
                player.time_jump_detection_method = 'last_active_timestamp'
            else:
                player.time_jump_detection_method = 'normal_elapsed_time'

            # quiz_completion_method = current progress method
            if player.participant.vars.get('go_to_results', False):
                player.quiz_completion_method = 'time_expired_jump'
            elif player.round_number == C.NUM_ROUNDS:
                player.quiz_completion_method = 'normal_completion'
            else:
                player.quiz_completion_method = 'in_progress'

            # 3. Progress tracking variables
            progress_percentage = (player.round_number / C.NUM_ROUNDS) * 100
            player.participant.vars['progress_percentage'] = progress_percentage

            # 4. Save current round timestamp
            player.participant.vars[f'active_timestamp_round_{player.round_number}'] = current_time

            # 5. Detect session interruption (improved version)
            if player.round_number > 1:
                prev_round = player.round_number - 1
                prev_timestamp_key = f'active_timestamp_round_{prev_round}'
                if prev_timestamp_key in player.participant.vars:
                    prev_timestamp = player.participant.vars[prev_timestamp_key]
                    time_gap = current_time - prev_timestamp

                    if time_gap > 30:  # Consider interruption if gap exceeds 30 seconds
                        player.session_interruption_detected = True
                        if 'total_interruption_time' not in player.participant.vars:
                            player.participant.vars['total_interruption_time'] = 0
                        player.participant.vars['total_interruption_time'] += (time_gap - 30)  # Subtract normal thinking time
                        player.total_interruption_time = player.participant.vars['total_interruption_time']

            # Ensure interruption-related fields have default values
            if not hasattr(player, 'session_interruption_detected') or player.session_interruption_detected is None:
                player.session_interruption_detected = False

            if not hasattr(player, 'total_interruption_time') or player.total_interruption_time is None:
                player.total_interruption_time = player.participant.vars.get('total_interruption_time', 0)

            # 6. Status snapshot (for abnormal recovery)
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

            # ==========================================================================
            # Original logic remains unchanged, but with per-round update functionality added
            # ==========================================================================

            # Skip processing if player never reached this page
            if player.participant.vars.get('go_to_results',
                                           False) and player.round_number > player.participant.vars.get(
                'last_displayed_round', 0):
                return

            # Ensure participant.vars exists
            if not hasattr(player.participant, 'vars'):
                player.participant.vars = {}

            # Calculate time and save basic information
            start_time = player.participant.vars.get('page_start_time', time.time())
            question_time = time.time() - start_time
            player.question_time_spent = question_time

            # Store response time for each round
            round_time_key = f'question_time_spent_round_{player.round_number}'
            player.participant.vars[round_time_key] = question_time

            # Record current progress status every round in case of abnormal exit
            current_progress = {
                'last_completed_round': player.round_number,
                'current_score': player.participant.vars.get('score', C.INITIAL_SCORE),
                'questions_attempted': player.participant.vars.get('questions_attempted', 0),
                'total_time_so_far': time.time() - player.participant.vars.get('quiz_start_time', time.time())
            }

            # Save current progress to participant.vars
            player.participant.vars['quiz_progress'] = current_progress

            # Get the user's answer and the correct answer
            correct_answer = C.CORRECT_ANSWERS.get(player.round_number, -1)
            user_answer = player.field_maybe_none('user_answer')

            # New: Initialize counters (ensure correct initial values for each round)
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

            # Initialize score if it doesn't exist
            if 'score' not in player.participant.vars:
                player.participant.vars['score'] = C.INITIAL_SCORE

            # Only process answers if the page was actually displayed
            if not player.participant.vars.get('go_to_results', False):
                # Check if the answer was submitted or skipped
                if user_answer is None:
                    # Question was skipped
                    player.is_answer_correct = False
                    player.is_answer_wrong = False
                    player.participant.vars['skipped_questions_count'] += 1
                else:
                    # Question was answered
                    player.is_answer_correct = (user_answer == correct_answer)
                    player.is_answer_wrong = (user_answer != correct_answer)

                    if player.is_answer_correct:
                        player.participant.vars['correct_answers_count'] += 1
                    else:
                        player.participant.vars['wrong_answers_count'] += 1

                    # Track questions attempted - only count as attempted if user provided an answer
                    player.participant.vars['questions_attempted'] += 1

                # Update score: +1 for correct answer, -0.25 for wrong, 0 for skipped
                if player.is_answer_correct:
                    player.participant.vars['score'] += 1
                elif player.is_answer_wrong:
                    player.participant.vars['score'] -= 0.25
                # Skipped questions don't change score

                # Increment total questions (including skipped)
                player.participant.vars['total_questions_attempted_with_skipped'] += 1

            else:
                # Page was not displayed, don't count as skipped or answered
                player.is_answer_correct = False
                player.is_answer_wrong = False

            # New: Update statistical data in Player model every round (current round only)
            player.correct_answers_count = player.participant.vars['correct_answers_count']
            player.wrong_answers_count = player.participant.vars['wrong_answers_count']
            player.skipped_questions_count = player.participant.vars['skipped_questions_count']
            player.total_questions_attempted_with_skipped = player.participant.vars[
                'total_questions_attempted_with_skipped']

            # New: Update total_questions_attempted every round (current round only)
            player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)

            # New: Update final_score every round (current round only)
            player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)

            # Improved average time calculation logic (current round only)
            questions_attempted = player.participant.vars.get('questions_attempted', 0)
            if questions_attempted > 0:  # Avoid division by zero
                total_time_on_questions = 0
                for round_num in range(1, player.round_number + 1):
                    round_time_key = f'question_time_spent_round_{round_num}'
                    round_time = player.participant.vars.get(round_time_key, 0)
                    total_time_on_questions += round_time

                avg_time = total_time_on_questions / questions_attempted
                player.participant.vars['average_time_per_question'] = avg_time
                player.average_time_per_question = avg_time
                # Remove cross-round synchronization: no longer update all rounds
            else:
                # If no questions answered, set average time to 0
                player.participant.vars['average_time_per_question'] = 0
                player.average_time_per_question = 0

            # New: Calculate average time including skipped questions (current round only)
            total_questions_with_skipped = player.participant.vars.get('total_questions_attempted_with_skipped', 0)
            if total_questions_with_skipped > 0:  # Avoid division by zero
                total_time_on_all_questions = 0
                for round_num in range(1, player.round_number + 1):
                    round_time_key = f'question_time_spent_round_{round_num}'
                    round_time = player.participant.vars.get(round_time_key, 0)
                    total_time_on_all_questions += round_time

                avg_time_with_skipped = total_time_on_all_questions / total_questions_with_skipped
                player.participant.vars['average_time_per_question_with_skipped'] = avg_time_with_skipped
                player.average_time_per_question_with_skipped = avg_time_with_skipped
                # Remove cross-round synchronization: no longer update all rounds
            else:
                # If no questions attempted, set average time to 0
                player.participant.vars['average_time_per_question_with_skipped'] = 0
                player.average_time_per_question_with_skipped = 0

            # New: Update competition status related variables every round (comparison with opponent, current round only)
            player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
            opponent_score = C.INITIAL_SCORE

            # Get opponent information
            others = player.get_others_in_group()
            if others:
                opponent = others[0]
                opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)
                player.opponent_score = opponent_score  # Update opponent score every round

            # Judge current win/loss status every round
            if player_score > opponent_score:
                player.is_winner = True
                player.competition_result = "Currently leading!"
            elif player_score < opponent_score:
                player.is_winner = False
                player.competition_result = "Currently behind. Keep going!"
            else:
                player.is_winner = False  # Temporarily set to False in case of tie, final round will handle
                player.competition_result = "Currently tied!"

            # Remove cross-round synchronization: no longer synchronize all rounds' key variables

            # Check if time expired
            start_time = player.participant.vars.get('quiz_start_time', time.time())
            elapsed_time = int(time.time() - start_time)
            time_expired = elapsed_time >= C.TOTAL_TIME

            # If time is up and we're not on the last round, skip to the last round
            if time_expired and player.round_number < C.NUM_ROUNDS:
                # Force advancing to the results page by setting current round to last round
                player.participant.vars['go_to_results'] = True

            # If it's the last round or time ran out, ensure final results are recorded
            if player.round_number == C.NUM_ROUNDS or time_expired:
                # Ensure final_score and other key data are always recorded
                player.final_score = player.participant.vars.get('score', C.INITIAL_SCORE)
                player.total_questions_attempted = player.participant.vars.get('questions_attempted', 0)

                # Improved time calculation logic
                quiz_start_time = player.participant.vars.get('quiz_start_time', 0)
                current_time = time.time()
                elapsed_time = current_time - quiz_start_time

                # Detect time jump
                if player.participant.vars.get('go_to_results', False):
                    player.time_jump_occurred = True
                    player.quiz_completion_method = 'time_expired_jump'

                    # Use last active time to calculate real duration
                    if player.last_active_timestamp > 0:
                        real_duration = player.last_active_timestamp - quiz_start_time
                        player.time_jump_detection_method = 'last_active_timestamp'
                    else:
                        # Use accumulated time
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

                # Update participant.vars
                player.participant.vars['quiz_end_time'] = current_time
                player.participant.vars['quiz_total_time'] = player.total_time_spent

                # Ensure competition result data is saved
                if 'competition_results' not in player.participant.vars:
                    # Get and calculate necessary competition result data
                    player_score = player.participant.vars.get('score', C.INITIAL_SCORE)
                    questions_attempted = player.participant.vars.get('questions_attempted', 0)

                    # Try to get opponent information
                    opponent_score = C.INITIAL_SCORE
                    others = player.get_others_in_group()
                    if others:
                        opponent = others[0]
                        opponent_score = opponent.participant.vars.get('score', C.INITIAL_SCORE)

                        # Persist opponent score
                        player.opponent_score = opponent_score

                    # Determine win/loss
                    if player_score > opponent_score:
                        player.is_winner = True
                        result_message = "Congratulations! You won!"
                    elif player_score < opponent_score:
                        player.is_winner = False
                        result_message = "Unfortunately, you lost. Thank you for participating!"
                    else:
                        # Tie situation, use group method to handle
                        player.group.handle_tie()
                        # Since handle_tie has already set is_winner, tie_occurred and other fields and competition_results
                        # No need to set these fields here
                        return

                    # Persist competition result information to Player model
                    player.competition_result = result_message

                    # Save competition results
                    player.participant.vars['competition_results'] = {
                        'total_questions': C.NUM_ROUNDS,
                        'total_questions_attempted': questions_attempted,
                        'total_questions_attempted_with_skipped': player.participant.vars.get(
                            'total_questions_attempted_with_skipped', 0),
                        'player_score': player_score,
                        'opponent_score': opponent_score,
                        'result_message': result_message,
                        'is_winner': player.is_winner,
                        'total_time_spent': player.total_time_spent,
                        'correct_answers_count': player.participant.vars.get('correct_answers_count', 0),
                        'wrong_answers_count': player.participant.vars.get('wrong_answers_count', 0),
                        'skipped_questions_count': player.participant.vars.get('skipped_questions_count', 0),
                        'average_time_per_question': player.participant.vars.get('average_time_per_question', 0),
                        'average_time_per_question_with_skipped': player.participant.vars.get(
                            'average_time_per_question_with_skipped', 0)
                    }

        except Exception as e:
            # Log exception but don't interrupt code execution
            error_msg = f"Error in round {player.round_number}: {str(e)}"
            if not hasattr(player.participant, 'vars'):
                player.participant.vars = {}
            player.participant.vars['quiz_errors'] = player.participant.vars.get('quiz_errors', []) + [error_msg]

            # Modified: Ensure existing data can be saved even if errors occur (per-round update)
            if 'score' in player.participant.vars:
                player.final_score = player.participant.vars['score']
            else:
                player.final_score = C.INITIAL_SCORE

            if 'questions_attempted' in player.participant.vars:
                player.total_questions_attempted = player.participant.vars['questions_attempted']
            else:
                player.total_questions_attempted = 0

            # New: Update total_time_spent even if errors occur
            if 'quiz_start_time' in player.participant.vars:
                quiz_start_time = player.participant.vars['quiz_start_time']
                player.total_time_spent = time.time() - quiz_start_time
            else:
                player.total_time_spent = 0

            # New: Update statistical data even if errors occur (current round only)
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

            # New: Default values for per-round update variables in exception handling
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
