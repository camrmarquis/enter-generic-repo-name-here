from tabulate import tabulate
import numpy as np
import pandas as pd


def get_remaining_probs(remaining_probs, scraps, prob_for_this_pick):
    for i in range(3):
        # Identify the teams that have not been picked
        not_picked = [j for j, e in enumerate(remaining_probs) if e != 0]
        pick = min(not_picked)

        scraps[i][pick] = scraps[i][pick] + prob_for_this_pick

        remaining_probs[pick] = 0.0
    return scraps

def main():
    df = pd.DataFrame(columns=['Seed', '1st Pick', '2nd Pick', '3rd Pick', '4th Pick',
                               '5th Pick', '6th Pick'])
    df['Seed'] = range(1, 7)

    initial_probs = [0.4, 0.33, 0.23, 0.02, 0.013, 0.007]
    second_probs = list(np.zeros(6))
    third_probs = list(np.zeros(6))
    scraps = np.zeros(shape=(3, 6))

    df['1st Pick'] = initial_probs

    for i in range(6):
        # Remove I from consideration for the second pick
        first_picked = initial_probs[:i] + [0.0] + initial_probs[i + 1:]

        # Re-normalize so total probaility is 1
        total_prob_remaining = sum(first_picked)
        conditional_prob = [initial_probs[i] * (x / total_prob_remaining)
                            for x in first_picked]

        # Need to keep these dynamic through all iterations
        # Sum the probabilities through each iteration
        second_probs = [x + y for x, y in zip(second_probs, conditional_prob)]

        for j in range(6):
            if i is not j:
                # Remove second pick j from consideration
                second_picked = first_picked[:j] + [0.0] + first_picked[j + 1:]

                # Re-normalize
                total_prob_remaining = sum(second_picked)
                conditional_prob_2 = [conditional_prob[j] * (x / total_prob_remaining)
                                      for x in second_picked]
                third_probs = [x + y for x, y in zip(third_probs, conditional_prob_2)]

                for k in range(6):
                    # Repeat same process again
                    if i is not k and j is not k:
                        third_picked = second_picked[:k] + [0.0] + second_picked[k + 1:]
                        scrap_prob = conditional_prob_2[k]

                        print(third_picked)

                        scraps = get_remaining_probs(remaining_probs=third_picked, scraps=scraps,
                                                     prob_for_this_pick=scrap_prob)

    df['2nd Pick'] = second_probs
    df['3rd Pick'] = third_probs
    df['4th Pick'] = scraps[0]
    df['5th Pick'] = scraps[1]
    df['6th Pick'] = scraps[2]

    columns = df.columns.values[1:]
    tol = 1e-6
    for column in columns:
        total = np.sum(df[column])
        if 1 - tol < total < 1 + tol:
            print(f'Total probability for column "{column}" sums to 1 (within tolerance)')
            continue
        else:
            raise ValueError(f'Probability for column "{column}" does not sum to 1')

    print(tabulate(df, tablefmt="pipe", headers="keys"))


if __name__ == "__main__":
    main()
