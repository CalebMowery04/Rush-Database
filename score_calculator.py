import csv


class Rush:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.cut = False
        self.scores = [0, 0, 0]
        self.interactions = [0, 0, 0]
        self.total_interactions = 0
        self.interaction_names = []
        self.db_score = 0
        self.comments = ""
        self.major = ""
        self.year = ""
        self.previously_knowns = ""
        self.clubs = ""
        self.gpa = 0.0
        self.interview_score = 0
        self.head_interviewer = ""
        self.pm_score = 0
        self.rush_score = 0
        self.rush_week_score = 0
        self.brotherhood_vote = ""

    def __repr__(self):
        return (
            self.name
            + " "
            + self.id
            + " "
            + str(self.cut)
            + " "
            + str(self.scores)
            + " "
            + str(self.interactions)
            + " "
            + str(self.db_score)
            + " "
            + str(self.interview_score)
            + " "
            + str(self.pm_score)
            + " "
            + str(self.rush_score)
            + " "
            + str(self.comments)
        )


# CHANGE THESE =================================================================================
rush_profile_filename = "real_data/rush_profile.csv"

sd_scores_filename = "real_data/sd_results.csv"
mingle_scores_filename = "real_data/bm_results.csv"
bbq_scores_filename = "real_data/bbq_results.csv"

# no votes used since fa 22
# votes_filename = ["real_data/vote_responses_1.csv", "real_data/vote_responses_2.csv", "real_data/vote_responses_3.csv"]  

interview_responses_filename = "real_data/adjusted_interview_scores.csv"
rush_scores_filename = "real_data/rush_scoring.csv"
pm_scores_filename = "real_data/pm_scoring.csv"

cut_sheet_filename = "real_data/cut_cleaned.csv"
cut_sheet_2_filename = "cut_2_cleaned.csv"

slides_info_filename = "real_data/slides_info.csv" # output file
db_final_filename = "real_data/db_final_final.csv" # output file
# ==============================================================================================

cut_sheets = [cut_sheet_filename]

score_filenames = [
    sd_scores_filename,
    mingle_scores_filename,
    bbq_scores_filename,
]

rushes = []

# rush profile data
with open(rush_profile_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

for row in data[1:]:
    found = False
    for rush in rushes:
        if rush.id == row[2].lower():
            found = True
    if not found:
        new_rush = Rush(row[1], row[2].lower())
        new_rush.major = row[4]
        new_rush.year = row[7]
        new_rush.previously_knowns = row[8]
        new_rush.clubs = row[9]
        new_rush.gpa = row[10]
        new_rush.email = row[3]
        rushes.append(new_rush)

# event data
for i in range(3):
    # get csv of scores from an event
    with open(score_filenames[i], newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    # add scores to local data
    for row in data:
        for rush in rushes:
            if rush.id == row[1]:
                rush.scores[i] = float(row[2])
                rush.interactions[i] = int(row[4])
                rush.total_interactions += int(row[4])
                # try block just for testing
                try:
                    list_names = row[5].split(",")
                    for name in list_names:
                        if name.strip() not in rush.interaction_names:
                            rush.interaction_names.append(name.strip())
                except:
                    print('some error')
                    None
                if row[3] != "":
                    if rush.comments == "":
                        rush.comments = row[3]
                    else:
                        rush.comments = rush.comments + " | " + row[3]
                break

# tally up event scores
for rush in rushes:
    score_sum = 0
    interactions = 0
    for i in range(3):
        # database scores are weighted based on the number of interactions at each event
        score_sum += rush.scores[i] * rush.interactions[i]
        interactions += rush.interactions[i]
    if interactions > 0:
        rush.db_score = score_sum / interactions

# parse cuts
with open(cut_sheet_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)
for row in data:
    if row[7] == "T":
        id = row[1].lower()
        for rush in rushes:
            if rush.id == id:
                rush.cut = True
                break

# parse cuts 2
if cut_sheet_2_filename != "":
    with open(cut_sheet_2_filename, newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    for row in data:
        if row[10] == "T":
            id = row[1].lower()
            for rush in rushes:
                if rush.id == id:
                    rush.cut = True
                    break

# parse pm scores
with open(pm_scores_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

for row in data[1:]:
    for rush in rushes:
        if rush.id == row[1]:
            if row[2] != '':
                rush.pm_score = float(row[2])
            break

# parse rush scores
with open(rush_scores_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

for row in data[1:]:
    for rush in rushes:
        if rush.id == row[1]:
            print(rush)
            rush.rush_score = float(row[2])
            break

# parse interview scores
with open(interview_responses_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

for row in data[1:]:
    for rush in rushes:
        if rush.id == row[1]:
            if row[3] != '':
                rush.interview_score = float(row[3])
                rush.head_interviewer = row[2]
            break

# BROTHERHOOD VOTE REMOVED FA 22
'''
# parse brotherhood vote
for i in range(3):
    with open(votes_filename[i], newline="") as f:
        reader = csv.reader(f)
        data = list(reader)

    for col in range(2, len(data[0])):
        for row in range(len(data)):
            # id case
            if col % 2 == 0:
                if row == 0:
                    header = data[0][col]
                    split_data = header.split("/")
                    name = split_data[0]
                    id = split_data[1]
                    current_id = id
                    running_votes, running_total = 0, 0
            # votes case
            else:
                if data[row][col] == "Yes Bro :)":
                    running_votes += 1
                    running_total += 1
                elif data[row][col] == "No Bro :(":
                    running_total += 1
                if row == len(data) - 1:
                    for rush in rushes:
                        if rush.id == current_id:
                            rush.brotherhood_vote = (
                                str(running_votes) + "/" + str(running_total)
                            )
                            break
'''

# **************** THESE WEIGHTINGS CAN CHANGE SEMESTER TO SEMESTER ****************
for rush in rushes:
    rush.rush_week_score = (
        0.5 * rush.db_score
        + 0.03 * rush.interview_score # extra 0 because interview scores are 0-10
        + 0.1 * rush.pm_score
        + 0.1 * rush.rush_score
    )

rushes.sort(key=lambda r: r.rush_week_score, reverse=True)

with open(slides_info_filename, "w") as csvfile:

    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        [
            "Name",
            "id",
            "Cut",
            "DB Score",
            "Interview",
            "Head Interviewer",
            "PM",
            "Rush",
            "Rush Week Score",
            "Major",
            "Year",
            "Previously Knowns",
            "Clubs",
            "GPA",
            "Unique Interactions",
        ]
    )

    for rush in rushes:
        if not rush.cut:
            csv_writer.writerow(
                [
                    rush.name,
                    rush.id,
                    rush.cut,
                    rush.db_score,
                    rush.interview_score,
                    rush.head_interviewer,
                    rush.pm_score,
                    rush.rush_score,
                    round(100 * rush.rush_week_score, 2),
                    rush.major,
                    rush.year,
                    rush.previously_knowns,
                    rush.clubs,
                    rush.gpa,
                    len(rush.interaction_names),
                ]
            )

with open(db_final_filename, "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        [
            "Name",
            "id",
            "Cut",
            "DB Score",
            "Interview",
            "Head Interviewer",
            "PM",
            "Rush",
            "Rush Week Score",
            "Major",
            "Year",
            "Previously Knowns",
            "Clubs",
            "GPA",
            "Unique Interactions",
            "Comments",
        ]
    )

    for rush in rushes:
        if not rush.cut:
            csv_writer.writerow(
                [
                    rush.name,
                    rush.id,
                    rush.cut,
                    rush.db_score,
                    rush.interview_score,
                    rush.head_interviewer,
                    rush.pm_score,
                    rush.rush_score,
                    rush.rush_week_score,
                    rush.major,
                    rush.year,
                    rush.previously_knowns,
                    rush.clubs,
                    rush.gpa,
                    len(rush.interaction_names),
                    rush.comments,
                ]
            )
