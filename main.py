# -*- coding: utf-8 -*-
#プレイヤーは2人を想定
import random

class Card():
	def __init__(self, color='b', number=0):
		self.color = color
		self.number = number
		self.is_open = False
	
	def __str__(self):
		return '({}, {}, {})'.format(self.color, self.number, self.is_open)
	
	def __repr__(self):
		return str(self)
	
	def __eq__(self, other):
		return self.color == other.color and self.number == other.number
	
	def __lt__(self, other):
		if self.number == other.number:
			#'black' < 'white' is True
			return self.color < other.color
		return self.number < other.number
	
	def __le__(self, other):
		if self.number == other.number:
			return self.color < other.color
		return self.number <= other.number
	
	def __gt__(self, other):
		if self.number == other.number:
			return self.color > other.color
		return self.number > other.number
	
	def __ge__(self, other):
		if self.number == other.number:
			return self.color > other.color
		return self.number >= other.number


deck = []				# 山札
player_hand = []		# プレイヤーの手札
ai_hand = []			# CPの手札
ai_known = []	# CP側から絶対にないとわかっているカード
player_saids = []		# playerがアタック時に言ったカード


def init_deck():
	global deck
	deck = []
	b = [Card('b', number) for number in range(0, 12)]
	w = [Card('w', number) for number in range(0, 12)]
	deck.extend(b)
	deck.extend(w)

def init_hands():
	global player_hand, ai_hand
	player_hand = [draw_card() for i in range(4)]
	player_hand.sort()
	ai_hand = [draw_card() for i in range(4)]
	ai_hand.sort()

def init_ai():
	global ai_known, ai_hand
	ai_known = []
	for card in ai_hand:
		ai_known.append(card)

def init_game():
	init_deck()
	init_hands()
	init_ai()
	player_attacks = []

def draw_card():
	global deck
	h_l = random.choice(deck)
	deck.remove(h_l)
	return h_l

def forecast_first(hand):
	"""
	手札(hand)の各カードにおいて、可能性のある数字のうち最も小さい数字を求め、リストにして返す
	"""
	firsts = []
	for i in range(len(hand)):
		first = 0
		if i == 0:#0の可能性がない場合でも0になるのでは?と思ったけど多分大丈夫
			firsts.append(first)
			continue
		if hand[i-1].is_open:
			first = hand[i-1].number
		else:
			first = firsts[i-1]
		if hand[i].color == 'w' and hand[i-1].color == 'b':
			firsts.append(first)
		else:
			firsts.append(first + 1)
	"""
	#下のコードでもできるが明らかに無意味に難しい
	#wのカードを見る時、前のwの数とbの塊ごとに塊内のbの数-1個を足したもの
	#bのカードを見る時、前のbの数とwの塊ごとに塊内のwの数-1個を足したもの
	for i in range(len(hand)):
		#手札の最初のカードなら0
		if i == 0:
			firsts.append(0)
		else:
			to_check = hand[:i+1] #最小のカードを調べるのに使うカード
			card_color = to_check[-1].color
			#予想中のカードと同じ色のカードのインデックスを抽出
			same_colors = [i for i in range(len(to_check)) if to_check[i].color == card_color]
			inv_count = 0 #inv_countには調べているカードの色
			#print(card_color, same_colors)
			for j in range(len(same_colors)):
				if same_colors[j] == 0: #カードが手札の先頭のカードであれば
					continue
				if j == 0: #最初に出てくる同色のカードであれば
					sandwitched = same_colors[j]
					if to_check[same_colors[j]].color == 'w':
						sandwitched -= 1
				else:
					sandwitched = same_colors[j] - same_colors[j-1] - 2
					#ここは必要だと思ってたけど動かしてみたらいらないことがわかった
					#if card_color == 'b' and sandwitched == 0:
						#sandwitched = 1
					if sandwitched < 0:
						sandwitched = 0 #負の値を足すのを防ぐ
				inv_count += sandwitched
			first_card = len(same_colors) - 1 + inv_count #-1で自身を除く
			firsts.append(first_card)
	"""
	return firsts

def forecast_last(firsts, hand):
	"""
	firstと同じような感じで
	"""
	lasts = []
	for i in range(len(hand))[::-1]:
		last = 11
		if i == len(hand)-1:
			lasts.append(last)
			continue
		if hand[i+1].is_open:
			last = hand[i+1].number
		else:
			last = lasts[len(hand)-1 - i - 1]
		if hand[i].color == 'b' and hand[i+1].color == 'w':
			lasts.append(last)
		else:
			lasts.append(last - 1)
	"""
	#各カードにおいて求めた予想の最小値全体の最大値を11から引いた値をその最小値に足したものが最大値
	max = firsts[-1]
	lasts = [first + (11 - max) for first in firsts]
	"""
	return lasts[::-1]

def forecast_card(hand, knowns, player_saids):
	"相手の手札の全てについての予想を返す"
	ai_forecasts = []
	firsts = forecast_first(hand)
	lasts = forecast_last(firsts, hand)
	for i in range(len(hand)):
		forecast = list(range(firsts[i], lasts[i]+1))
		knowns_same_color = [card.number for card in knowns if card.color == hand[i].color]
		said_same_color = [card.number for card in player_saids if card.color == hand[i].color]
		for known in knowns_same_color:
			try:
				forecast.remove(known)
			except ValueError:
				pass
		for said in said_same_color:
			try:
				forecast.remove(said)
			except ValueError:
				pass
		#予想がなくなった場合に相手の言ったカードが相手の手札にふくまれている可能性があるのでそれに対処する
		if not forecast:
			for said in said_same_color:
				if said not in knowns_same_color:
					forecast.append(said)
			forecast.sort()
		ai_forecasts.append(forecast)
	return ai_forecasts

def check_all_opend(hand):
	is_opens = [card.is_open for card in hand]
	all_opend = True
	for is_open in is_opens:
		all_opend = all_opend and is_open
	return all_opend

def show_hands():
	global player_hand, ai_hand
	show_ai_hand = []
	for c in ai_hand:
		t = c.color,  str(c.number) if c.is_open else '?', ' '
		show_ai_hand.append(''.join(t))#tupleのlistになってる
	show_player_hand = []
	for c in player_hand:
		t = c.color, str(c.number), 'x' if c.is_open else 'o'
		show_player_hand.append(''.join(t))
	print('ai_hand     : ', show_ai_hand)
	print('player_hand : ', show_player_hand)

def ai_turn(is_first_turn = False, drawed_card = None):
	global ai_hand, player_hand
	global ai_known, player_saids
	if is_first_turn:
		draw = draw_card()
		ai_known.append(draw)
	else:
		draw = drawed_card
	ai_forecasts = forecast_card(player_hand, ai_known, player_saids)
	
	#TODO: ここに再攻撃するかどうかの判定入れる

	#最も候補の少ないカードを攻撃対象とする
	min_f = 0
	while len(ai_forecasts[min_f]) == 0 or player_hand[min_f].is_open:
		min_f += 1
	for i in range(len(ai_forecasts)):
		if not player_hand[i].is_open:
			if len(ai_forecasts[i]) < len(ai_forecasts[min_f]):
				min_f = i
	
	#各候補の正解する確率は同一なのでランダムにアタックで使う数字を決定する
	choiced_num = random.choice(ai_forecasts[min_f])
	choiced_card = Card(player_hand[min_f].color, choiced_num)
	ai_known.append(choiced_card)
	print('CP < Is {} {}? {}'.format(min_f, choiced_num, player_hand[min_f].number == choiced_num))
	if player_hand[min_f].number == choiced_num:
		player_hand[min_f].is_open = True

		#プレイヤーの手札が全て開いていれば終了する
		if check_all_opend(player_hand):
			return 'cp'
		#もう一度ターンを行う
		return ai_turn(False, draw)
	else:
		draw.is_open = True
		ai_hand.append(draw)
		ai_hand.sort()
		return 'continue'

def player_turn(is_first_turn = False, drawed_card = None):
	global ai_hand, player_hand
	global ai_known, player_saids

	if is_first_turn:
		draw = draw_card()
	else:
		draw = drawed_card
	#入力
	#TODO: この辺を書き換えて、手札に戻すという選択を取れるようにする
	show_text = 'drawed "{}". input [place num] : '.format(''.join((draw.color, str(draw.number))))
	while True:
		try:
			place, number = [int(s) for s in input(show_text).split()]
		except ValueError:
			print('place and number must be integer.  please input again')
			continue
		break
	print('Is {} {}? {}'.format(place, number, ai_hand[place].number == number))
	if ai_hand[place].number == number:
		ai_hand[place].is_open = True
		show_hands()

		if check_all_opend(ai_hand):
			return 'player'
		return player_turn(False, draw)
	else:
		draw.is_open = True
		ai_known.append(draw)
		player_hand.append(draw)
		player_hand.sort()
		return 'continue'


def game_loop(first_turn):
	global player_hand, ai_hand
	turn = first_turn
	while True:
		show_hands()
		if turn == 'player':
			game_status = player_turn(is_first_turn = True)
		else:
			game_status = ai_turn(is_first_turn = True)
		if game_status != 'continue':
			return game_status
		turn = 'player' if turn == 'cp' else 'cp'

def main():
	global ai_hand
	init_game()
	if random.randint(0,1):
		first_turn = 'player'
	else:
		first_turn = 'cp'
	winner = game_loop(first_turn)
	
	if winner == 'cp':
		for card in ai_hand:
			card.is_open = True
		print('\nThis is answer.')
		show_hands()
		print('YOU LOSE...')				
	else:
		print('YOU WIN!!!')

if __name__ == '__main__':
	main()
