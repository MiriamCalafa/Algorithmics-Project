import random
import itertools

# Create an Italian 40-card deck
suits = ['Quadri', 'Picche', 'Cuori', 'Fiori']
values = ['Asso', '2', '3', '4', '5', '6', '7', 'Jack', 'Donna', 'Re']

def initialize_game(mode):
    # Shuffle the deck
    deck = [{'value': value, 'suit': suit} for value in values for suit in suits]
    random.shuffle(deck)
    players_hands=[[],[]]
    player1_name = input("Enter the name for Player 1: ")
    if mode==1:
      player2_name = input("Enter the name for Player 2: ")
    else:
      player2_name = ""
    # Draw four cards and place them face-up on the table
    table_cards = [deck.pop() for _ in range(4)]

    # Initialize scores and collected cards for each player
    total_scores = [0, 0]
    collected_cards = [[],[]]

    return deck, total_scores, collected_cards, table_cards, players_hands, player1_name, player2_name

# Deal three cards to each player
def deal_cards(deck, num_players, num_cards):
    hands = [[] for _ in range(num_players)]

    for _ in range(num_cards):
        for player in range(num_players):
            card = deck.pop()
            hands[player].append(card)

    return hands

def beggin_of_turn(deck, table_cards, players_hands):
    # Check if the player's hand is empty before dealing new cards
    for i in range(len(players_hands)):
        if not players_hands[i] and deck:
            # Deal three cards to the player if the hand is empty and the deck is not empty
            players_hands[i] = [deck.pop() for _ in range(3)]

    return deck, players_hands, table_cards


def card_value(card):
    # Helper function to get the numerical value of a card
    if card['value'] == 'Jack':
        return 8
    elif card['value'] == 'Donna':
        return 9
    elif card['value'] == 'Re':
        return 10
    elif card['value'] == 'Asso':
        return 1
    else:
        return int(card['value'])

def check_settebello(player_collection, total_score0, total_score1):
    # Check if the player has the Settebello card (7 of coins)
    settebello_card = {'value': '7', 'suit': 'Fiori'}
    if settebello_card in player_collection:
      total_score0+=1
      #print("7b player1")
    else:
      total_score1+=1
      #print("7b player2")
    return total_score0, total_score1


def primiera_value (card):
    if card['value'] == 'Jack':
        return 10
    elif card['value'] == 'Donna':
        return 10
    elif card['value'] == 'Re':
        return 10
    elif card['value'] == 'Asso':
        return 16
    elif card['value'] == '7':
        return 21
    elif card['value'] == '6':
        return 18
    else:
        return 0

def calculate_primiera_score(player_collection0, player_collection1, total_score0, total_score1):
    primiera_values = ['7', '6', 'Asso', 'Jack', 'Donna', 'Re']
    primiera_score0=primiera_valuee(player_collection0)
    primiera_score1=primiera_valuee(player_collection1)
    #print("primiera: ", primiera_score0, primiera_score1)

    if primiera_score0 > primiera_score1:
        total_score0 += 1
    elif primiera_score1 > primiera_score0:
        total_score1 += 1

    return total_score0, total_score1

def primiera_valuee (collection):
  primiera_values = ['7', '6', 'Asso', 'Jack', 'Donna', 'Re']
  suits = ['Quadri', 'Picche', 'Cuori', 'Fiori']
  sum=0

  for value in primiera_values:
    for suit in suits:
        card = {'value': value, 'suit': suit}
        if card in collection:
            if value == 'Donna' or value == 'Re' or value == 'Jack':
                sum+= 10
            elif value == 'Asso':
                sum+= 16
            elif value == '7':
                sum+= 21
            elif value == '6':
                sum+= 18
  return sum


def calculate_ori_score(player_collection0, player_collection1, total_score0, total_score1):
  ori_score0=ori_valuee(player_collection0)
  ori_score1=ori_valuee(player_collection1)
  #print("ori: ", ori_score0, ori_score1)
  if ori_score0 > ori_score1:
      total_score0 += 1
  elif ori_score1 > ori_score0:
      total_score1 += 1

  return total_score0, total_score1

def ori_valuee (collection):
  ori_values = ['2', '3', '4', '5','7', '6', 'Asso', 'Jack', 'Donna', 'Re']
  sum=0

  for value in ori_values:
    #for suit in suits:
        card = {'value': value, 'suit': 'Quadri'}
        if card in collection:
            sum+= 1
  return sum


def determine_winner(total_scores):
    # Determine the winner based on total scores
    if total_scores[0] > total_scores[1]:
        print("Player 1 wins!")
    elif total_scores[1] > total_scores[0]:
        print("Player 2 wins!")
    else:
        print("It's a tie!")

def calculate_points(total_scores0, total_scores1,collected_cards0, collected_cards1, player1_name, player2_name):
    print("Scopa:",total_scores0, total_scores1)

    # Calculate Settebello and Primiera scores at the end of the game
    total_scores0, total_scores1=check_settebello(collected_cards0, total_scores0, total_scores1)
    print("Settebello:", total_scores0, total_scores1)

    total_scores0, total_scores1= calculate_primiera_score(collected_cards0, collected_cards1, total_scores0, total_scores1)
    print("Primiera:", total_scores0, total_scores1)

    # Determine Carte
    if len(collected_cards0)> len(collected_cards1):
      total_scores0+=1
    if len(collected_cards0)< len(collected_cards1):
      total_scores1+=1
    print("Carte:", total_scores0, total_scores1)
    #print("carte",len(collected_cards0),len(collected_cards1) )

    # Determine Ori
    total_scores0, total_scores1= calculate_ori_score(collected_cards0, collected_cards1, total_scores0, total_scores1)
    print("Ori:", total_scores0, total_scores1)

    # Display the final scores
    print("Final Scores", player1_name,":", total_scores0)
    print("Final Scores", player2_name,":", total_scores1)
    return


import itertools

def play_turn(player_hand, table_cards, player_collection, total_scores):
    while True:
        # Display the current state of the game
        print("Table cards:", [f"{card['value']}, {card['suit']}" for card in table_cards])
        print("Your hand:", [f"{card['value']}, {card['suit']}" for card in player_hand])
        try:
            # Allow the player to play a card from their hand
            selected_card_index = int(input("Select the index of the card you want to play (0 to {}): ".format(len(player_hand) - 1)))
            # Get the selected card
            played_card = player_hand.pop(selected_card_index)
            # Determine if the played card captures other cards on the table based on value
            captured_cards = []
            # First, try to capture cards with the same value
            matching_value_cards = [card for card in table_cards if card_value(played_card) == card_value(card)]
            if matching_value_cards:
                if len(matching_value_cards) > 1:
                    # Case 1: Multiple cards with the same value, prompt the player to choose
                    print("Multiple cards with the same value. Choose which card to capture:")
                    for i, card_on_table in enumerate(matching_value_cards):
                        print(f"{i+1}: {card_on_table['value']}, {card_on_table['suit']}")
                    choice = int(input("Enter the number of the card you want to pick: ")) - 1
                    captured_cards.extend(matching_value_cards[choice])
                else:
                    # Case 2: Only one card with the same value
                    captured_cards.extend(matching_value_cards)
            # If no cards with the same value, try combinations
            if not captured_cards:
                valid_combinations = []
                for combination_size in range(1, len(table_cards) + 1):
                    # Try all combinations of the cards on the table
                    for combination in itertools.combinations(table_cards, combination_size):
                        if card_value(played_card) == sum(card_value(captured_card) for captured_card in combination):
                            # The played card can capture the combination of cards on the table
                            valid_combinations.append(list(combination))
                if valid_combinations:
                    if len(valid_combinations) > 1:
                        # Case 3: Multiple valid combinations, prompt the player to choose
                        print("Multiple valid combinations. Choose which cards to capture:")
                        for i, combination in enumerate(valid_combinations):
                            formatted_combination = [f"{card['value']}, {card['suit']}" for card in combination]
                            print(f"{i+1}: {formatted_combination}")
                        choice = int(input("Enter the number of the combination you want to pick: ")) - 1
                        chosen_combination = valid_combinations[choice]
                        # Remove selected cards from the table
                        for card_on_table in chosen_combination:
                            table_cards.remove(card_on_table)
                        # Add selected cards to the player's collection
                        captured_cards.extend(chosen_combination)
                    else:
                        chosen_combination = valid_combinations[0]
                        # Remove selected cards from the table
                        for card_on_table in chosen_combination:
                            table_cards.remove(card_on_table)
                        # Add selected cards to the player's collection
                        captured_cards.extend(chosen_combination)
                else:
                    # Case 4: No valid combinations or only one valid combination
                    print("No matching value on the table. The card has been added to the table.")
                    table_cards.append(played_card)
            if len(captured_cards) > 0:
                # Case 5: The played card captures cards with the same value
                print("You captured the following cards:", [f"{card['value']}, {card['suit']}" for card in captured_cards])
                captured_indices = []
                for captured_card in captured_cards:
                    # Find the index of the captured card in the table
                    indices = [i for i, card in enumerate(table_cards) if card == captured_card]
                    captured_indices.extend(indices)
                # Remove captured cards from the table in reverse order to avoid index issues
                for index in sorted(captured_indices, reverse=True):
                    table_cards.pop(index)
                for captured_card in captured_cards:
                    player_collection.append(captured_card)
                player_collection.append(played_card)
                if not table_cards:
                    print("Scopa! You get 1 point.")
                    total_scores += 1
            return captured_cards, total_scores, player_collection, table_cards
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid index.")
            continue


def play_game_AI():
    # Initialize the game
    deck, total_scores, collected_cards, table_cards, players_hands, player1_name, player2_name = initialize_game(0)
    last=0

    # Play multiple rounds until the deck is empty
    while deck or any(players_hands):
        # Begin Player 1's turn
        deck, players_hands, table_cards = beggin_of_turn(deck, table_cards, players_hands)

        # Player 1 plays their turn
        print("\n-------------------------------------------------------------------------------------------------------\n", player1_name, ":")
        captured_cards, total_scores[0], collected_cards[0], table_cards = play_turn(players_hands[0], table_cards, collected_cards[0], total_scores[0])

        # Save the captured cards for Player 1
        if len(captured_cards)>0:
          last=1

        # Begin Player 2's turn
        print("\n-------------------------------------------------------------------------------------------------------\nPlayer2/AI:")
        deck, players_hands, table_cards = beggin_of_turn(deck, table_cards, players_hands)

        # Player 2 plays their turn
        play_card, matching= AI (table_cards, players_hands[1], collected_cards[0], collected_cards[1])
        players_hands[1],captured_cards, total_scores[1] = play_turn_AI(players_hands[1], table_cards, collected_cards[1], total_scores[1], play_card, matching)

        # Save the captured cards for Player 2
        if len(captured_cards)>0:
          last=2
    for table_card in table_cards:
          collected_cards[last-1].append(table_card)
    print(collected_cards[0])
    print(collected_cards[1])
    calculate_points(total_scores[0], total_scores[1],collected_cards[0], collected_cards[1])

def play_turn_AI(player_hand, table_cards, player_collection,total_scores, play_card, captured_cards):
    # Display the current state of the game
    player_hand.remove(play_card)
    print("Played card:", play_card)
    if len(captured_cards)<1:
      print("No matching value on the table. The card has been added to the table.")
      table_cards.append(play_card)
    else:
      print("You captured the following cards:")
      player_collection.append(play_card)
      for captured_card in captured_cards:
            print(f"{captured_card['value']}, {captured_card['suit']}")
            table_cards.remove(captured_card)
            player_collection.append(captured_card)

      if (len(table_cards)==0):
        print("Scopa!")
        total_scores+=1
    return player_hand, captured_cards, total_scores

def AI (table, hand, collected0, collected1):
  hand_indices=[]
  #print("Table:", table, "\nHand:", hand )
  backup_hand=hand
  backup_table=table
  backup_c0=collected0
  backup_c1=collected1
  played_card=[]
  points=[]
  print("Table cards:", [f"{card['value']}, {card['suit']}" for card in table])
  print("AI hand:", [f"{card['value']}, {card['suit']}" for card in hand])
  max_hand=len(hand)-1
  for index in range(max_hand, -1,-1):

    played_card = backup_hand.pop(index)
    #print(index, ") Analysis: ", [f"{played_card['value']}, {played_card['suit']}"])

    # Determine if the played card captures other cards on the table based on value
    captured_cards = []

    matching_value_cards=[]

    # First, try to capture cards with the same value
    for card in table:
      if card_value(played_card) == card_value(card):
        matching_value_cards.append(card)
        #print(card)
    #print("Matching values: ", matching_value_cards)

    if matching_value_cards:
        if len(matching_value_cards) > 1:

            for i in range(len(matching_value_cards)):
              captured_cards.append(matching_value_cards[i])
              point=valuate(played_card, captured_cards, backup_hand, backup_table, backup_c0, backup_c1)
              points.append([played_card, captured_cards,point])
              captured_cards.remove(matching_value_cards[i])
        else:
            # Case 2: Only one card with the same value
            captured_cards.append(matching_value_cards)
            point=valuate(played_card, matching_value_cards, backup_hand, backup_table, backup_c0, backup_c1)
            points.append([played_card, matching_value_cards,point])
            captured_cards.remove(matching_value_cards)
    # If no cards with the same value, try combinations
    else:
        valid_combinations = []

        for combination_size in range(1, len(table) + 1):
            # Try all combinations of the cards on the table
            for combination in itertools.combinations(table, combination_size):
                if card_value(played_card) == sum(card_value(captured_card) for captured_card in combination):
                    # The played card can capture the combination of cards on the table
                    valid_combinations.append(list(combination))
        #print("Valid Combos: ", valid_combinations)

        if valid_combinations :
            # Case 3: Multiple valid combinations, prompt the player to choose
            for i in range(len(valid_combinations)):

              captured_cards.extend(valid_combinations[i])
              point=valuate(played_card, valid_combinations[i], backup_hand, backup_table, backup_c0, backup_c1)
              points.append([played_card, valid_combinations[i],point])
              #captured_cards.remove(valid_combinations[i])
              #print(captured_cards)
        else:
            # Case 4: No valid combinations
            #print("No combo")
            point=valuate(played_card, matching_value_cards, backup_hand, backup_table, backup_c0, backup_c1)
            points.append([played_card, matching_value_cards, point])
    backup_hand.insert(index, played_card)
  #for oint in points:
  #  print (oint) ###############################################################
  #print (points)
  for entry in points:
        played_card_str = f"{entry[0]['value']}, {entry[0]['suit']}"
        matching_cards_str = [f"{card['value']}, {card['suit']}" for card in entry[1]]
        print(f"Played: {played_card_str}, Matching: {matching_cards_str}, Points: {entry[2]}")
  max_point_entry = max(points, key=lambda entry: entry[2])
  max_played_card, max_matching_value_cards, max_point = max_point_entry
  print("\nMax Point:", max_point)
  print("Played Card:", [f"{max_played_card['value']}, {max_played_card['suit']}"])
  print("Matching Value Cards:", [f"{card['value']}, {card['suit']}" for card in max_matching_value_cards], "\n")


  return max_played_card, max_matching_value_cards

def valuate (played_card, matching, hand, table, collected0, collected1):
  point=0
  nowtable=[]
  for card in table:
      nowtable.append(card)
  if len(matching)>0:
    for match in matching:
      #for table_card in table:
        if(match in nowtable):
          nowtable.remove(match)
          #print("carta rimossa dal tavolo")
  #print(nowtable)
  nowhand=hand

  if len(matching)<1:
    nowtable.append(played_card)
    point-=5*oro(played_card)
    #print("no matching ", point)
    point-=7*settes(played_card)
    #print("no matching ", point)

  else:
    point+=len(matching)
    #print("matching ", point)
    point+=3*ori(matching)
    #print("matching ", point)
    point+=3*oro(played_card)
    #print("matching ", point)
    point+=5*sette(matching)
    #print("matching ", point)
    point+=5*settes(played_card)
    #print("matching ", point)
    if (len(nowtable)==0):
      point+=10
      #print("scopa ", point)
  point-=5*somma_table_7(nowtable, collected0, collected1, nowhand)
  #print("somma7 ", point)
  point-=5*somma_table_scopa(nowtable, collected0, collected1, nowhand)
  #print("somma scopa ", point)
  #print(played_card,"      ", matching,"      ", point, "\n")

  return point

def somma_table_7(table, collected0, collected1, hand):
  point=0
  #print(table)
  if (sette(collected0)+sette(collected1)+sette(table)+sette(hand)==4):
    return 0
  for combination_size in range(1, len(table) + 1):
    # Try all combinations of the cards on the table
    for combination in itertools.combinations(table, combination_size):
        if 7 == sum(card_value(card) for card in combination):
            # The played card can capture the combination of cards on the table
            point+=1

  return point

def somma_table_scopa(table, collected0, collected1, hand):
  point=0
  if sum(card_value(card) for card in table)>10:
    return 0
  play=sum(card_value(card) for card in table)
  if (val(play,collected0)+val(play,collected1)+val(play,table)+val(play,hand))==4:
    return 0
  return (4-(val(play,collected0)+val(play,collected1)+val(play,table)+val(play,hand)))

def ori (match):
  ori_values = ['2', '3', '4', '5','7', '6', 'Asso', 'Jack', 'Donna', 'Re']
  sum=0
  for value in ori_values:
    #for suit in suits:
        card = {'value': value, 'suit': 'Quadri'}
        if card in match:
          #print("preso oro", card)
          sum += 1
  return sum

def oro (card):
  ori_values = ['2', '3', '4', '5','7', '6', 'Asso', 'Jack', 'Donna', 'Re']
  for value in ori_values:
        oro = {'value': value, 'suit': 'Quadri'}
        if card == oro:
            return 1
  return 0

def sette (match):
  sum=0
  for suit in suits:
      card = {'value': '7', 'suit': suit}
      if (card in match):
            sum += 1
  return sum

def settes (card):
  for suit in suits:
      sette = {'value': '7', 'suit': suit}
      if sette==card:
            return 1
  return 0

def val (play,match):
  sum=0
  for suit in suits:
      card = {'value': play, 'suit': suit}
      if (card in match):
            sum += 1
  return sum

play_game_AI()

