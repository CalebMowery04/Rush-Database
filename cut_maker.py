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
        self.email = ""

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
sd_scores_filename = "real_data/bm_results.csv"
mingle_scores_filename = "real_data/sd_results.csv"

rush_profile_filename = "real_data/rush_profile.csv"

cut_sheet_filename = "real_data/cut.csv" # output file
# ==============================================================================================

score_filenames = [sd_scores_filename, mingle_scores_filename]

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
for i in range(len(score_filenames)):
    print('new event')
    # get csv of scores from an event
    with open(score_filenames[i], newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    # add scores to local data
    for row in data[1:]:
        found = False
        for rush in rushes:
            print(row)
            if rush.id == row[1].lower():
                found = True
                rush.scores[i] = float(row[2])
                rush.interactions[i] = int(row[4])
                rush.total_interactions += int(row[4])
                try:
                    list_names = row[5].split(",")
                    for name in list_names:
                        if name.strip() not in rush.interaction_names:
                            rush.interaction_names.append(name.strip())
                except:
                    None
                if row[3] != "":
                    if rush.comments == "":
                        rush.comments = row[3]
                    else:
                        rush.comments = rush.comments + " | " + row[3]
                break
        # this is the case where we have data about a rush from an event, but they haven't filled out the rush profile
        if not found:
            new_rush = Rush(row[0], row[1].lower())
            # print('not found', new_rush)
            rushes.append(new_rush)
            new_rush.scores[i] = float(row[2])
            new_rush.interactions[i] = int(row[4])
            new_rush.total_interactions += int(row[4])
            try:
                list_names = row[5].split(",")
                for name in list_names:
                    if name.strip() not in new_rush.interaction_names:
                        new_rush.interaction_names.append(name.strip())
            except:
                None
            if row[3] != "":
                if new_rush.comments == "":
                    new_rush.comments = row[3]
                else:
                    new_rush.comments = new_rush.comments + " | " + row[3]

# tally up event scores
for rush in rushes:
    score_sum = 0
    interactions = 0
    for i in range(2):
        score_sum += rush.scores[i] * rush.interactions[i]
        interactions += rush.interactions[i]
    if interactions > 0:
        rush.db_score = score_sum / interactions

rushes.sort(key=lambda r: r.db_score, reverse=True)

# write score breakdown
with open(cut_sheet_filename, "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        [
            "Name",
            "id",
            "Speed Dating Score",
            "Speed Dating Interactions",
            "Mingle Score",
            "Mingle Interactions",
            "Overall Score",
            "Cut",
            "Year",
            "GPA",
            "email"
        ]
    )
    for rush in rushes:
        csv_writer.writerow(
            [
                rush.name,
                rush.id,
                rush.scores[0],
                rush.interactions[0],
                rush.scores[1],
                rush.interactions[1],
                rush.db_score,
                "F",
                rush.year,
                rush.gpa,
                rush.email
            ]
        )
