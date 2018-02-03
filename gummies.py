# Benjamin Share 2/3/18

from scipy.special import comb as nCk
from matplotlib import pyplot as plt

def probOfDrawing(total_black, total_white, num_black, num_white):
	if num_black > total_black or num_white > total_white:
		raise Exception("Invalid input: (%d, %d, %d, %d)" % (total_black, total_white, num_black, num_white))

	total_options = nCk(total_black + total_white, num_black + num_white)
	valid_options = nCk(total_black, num_black) * nCk(total_white, num_white)

	return valid_options / total_options

def getTransitionProbs(total_black, total_white, num_to_draw):
	if num_to_draw > total_black + total_white:
		raise Exception("Invalid input: (%d, %d, %d)" %(total_black, total_white, num_to_draw))

	probs = {}
	for num_black in range(max(0, num_to_draw - total_white), min(num_to_draw, total_black) + 1):
		num_white = num_to_draw - num_black
		prob = probOfDrawing(total_black, total_white, num_black, num_white)
		probs[(num_black, num_white)] = prob

	return probs

def getExpectedGummies(initial_black, initial_white, num_to_draw, num_we_take):
	cache = {(0, 0): 0}

	def construct(total_black, total_white):
		key = (total_black, total_white)
		if key in cache:
			return

		transition_probs = getTransitionProbs(total_black, total_white, num_to_draw)

		expected_value = 0
		for possibility in transition_probs:
			gain = min(possibility[0], num_we_take)

			new_black = total_black - possibility[0]
			new_white = total_white - possibility[1]
			construct(new_black, new_white)
			expected_value += transition_probs[possibility] * (cache[(new_black, new_white)] + gain)

		cache[key] = expected_value

	construct(initial_black, initial_white)
	return cache[(initial_black, initial_white)]

def plotForDifferentStarts(total, num_to_draw, num_we_take):
	expected_of_total = [0]
	expected_of_available = [1]
	for num_black in range(1, total + 1):
		expected = getExpectedGummies(num_black, total - num_black, num_to_draw, num_we_take)
		expected_of_total.append(expected / total)
		expected_of_available.append(expected / num_black)

	plt.figure()
	plt.scatter(range(total + 1), expected_of_total)
	plt.scatter(range(total + 1), expected_of_available)
	plt.legend(["Fraction of total", "Fraction of available"])
	plt.xlabel("Number of desired gummies")
	plt.ylabel("Expected fraction recieved")
	plt.savefig("ConstantParams%d_%d_%d" %(total, num_to_draw, num_we_take))

# Assuming that total is even and we have a 50/50 split
def plotForDifferentParameters(total, max_draw=12):
	num_black = total / 2
	num_white = total / 2

	# Initialize to create a dummy zero value at (1, 2) so that the color scale has white at 0.
	draw_vals = [1]
	take_vals = [2]
	rewards = [0]

	for num_to_draw in range(1, max_draw + 1):
		if total % num_to_draw:
			# Haven't defined behavior when we have leftovers at the end.
			continue
		for num_we_take in range(1, num_to_draw + 1):
			draw_vals.append(num_to_draw)
			take_vals.append(num_we_take)
			rewards.append(getExpectedGummies(num_black, num_white, num_to_draw, num_we_take) / num_black)

	plt.figure()
	plt.scatter(draw_vals, take_vals, c=rewards, s=500, cmap='gray_r')
	plt.colorbar()
	plt.xlabel("Number of gummies drawn at once")
	plt.ylabel("Number of gummies we take")
	plt.savefig("VaryingParams%d" % total)

if __name__ == "__main__":
	# Answer to the original question:
	print "We expect %.3f gummies." % getExpectedGummies(30, 30, 4, 2)

	# And some extra visuals
	plotForDifferentStarts(60, 4, 2)
	plotForDifferentParameters(60)


