import csv


class Rush:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.score = 0
        self.comments = []
        self.interactions = 0
        self.interaction_names = []

    def __repr__(self):
        return (
            self.name
            + " "
            + str(self.id)
            + " "
            + str(self.score)
            + " "
            + str(self.comments)
        )


def convert_response(response):
    dict = {
        "Strongly Agree": 4,
        "Agree": 3,
        "Neutral": 2,
        "Disagree": 1,
        "Strongly Disagree": 0,
    }
    return dict[response]


def ingest(filenames, save_as):
    rushes = []
    for filename in filenames:
        with open(filename, newline="") as f:
            reader = csv.reader(f)
            data = list(reader)

        num_rows = len(data)

        running_points = 0
        running_possible_points = 0

        # this is a weird way to iterate, basically have to iterate by col, row rather than row, col because of how the sheets look from the forms
        for col in range(2, len(data[0])):
            for row in range(len(data)):
                # name:id case, initialize
                if col % 7 == 2:
                    if row == 0:
                        header = data[0][col]
                        split_data = header.split("/")
                        print(split_data)
                        name = split_data[0]
                        id = split_data[1]
                        new_rush = Rush(name, id)
                        rushes.append(new_rush)
                        current_rush = new_rush
                        running_points, running_possible_points, interactions = 0, 0, 0
                # skip comment col (1) and interact column (3)
                elif col % 7 != 1 and col % 7 != 3:
                    if row != 0:
                        response = data[row][col]
                        if response != "":
                            if col % 7 == 4:
                                current_rush.interaction_names.append(data[row][1].lower())
                            interactions += 1
                            running_points += convert_response(response)
                            running_possible_points += 4
                # we are at comment row, total points
                elif col % 7 == 1:
                    if row == 0:
                        comments = []
                        if running_possible_points > 0:
                            total_score = running_points / running_possible_points
                            current_rush.score = total_score
                        else:
                            current_rush.score = 0
                        # interactions is counted for each response so 4x too many
                        current_rush.interactions = int(interactions / 4)
                    # add all the comments
                    else:
                        if data[row][col] != "":
                            comments.append(data[row][1] + ": " + data[row][col])
                        if row == num_rows - 1:
                            s = ""
                            for comment in comments:
                                s += " | " + comment
                            s = s[2:]
                            current_rush.comments = s

    rushes.sort(key=lambda r: r.score, reverse=True)
    
    with open(save_as, "w") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(["Name", "id", "Score", "Comments", "Interactions", "Names"])
        for rush in rushes:
            # parse names into a string for csv export
            interaction_string = ""
            for name in rush.interaction_names:
                interaction_string += ", " + name
            interaction_string = interaction_string[2:]
            csvwriter.writerow(
                [
                    rush.name,
                    rush.id,
                    rush.score,
                    rush.comments,
                    rush.interactions,
                    interaction_string,
                ]
            )

# CHANGE THESE =================================================================================
event_responses_filenames = [
    "real_data/SD24 Scoring Form 0 (Responses) - Form Responses 1.csv",
    "real_data/SD24 Scoring Form 1 (Responses) - Form Responses 1.csv",
    "real_data/SD24 Scoring Form 2 (Responses) - Form Responses 1.csv",
    "real_data/SD24 Scoring Form 3 (Responses) - Form Responses 1.csv",
    "real_data/SD24 Scoring Form 4 (Responses) - Form Responses 1.csv",
    "real_data/SD24 Scoring Form 5 (Responses) - Form Responses 1.csv"
]
event_results_filename = "real_data/sd_results" # output file
# ==============================================================================================

rush_scores = ingest(event_responses_filenames, event_results_filename)
