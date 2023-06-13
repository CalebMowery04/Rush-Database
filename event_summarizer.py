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
sd_scores_filename = "real_data/sd_results_cleaned_final.csv"
mingle_scores_filename = "real_data/bm_results_cleaned.csv"
gn_scores_filename = "real_data/gn_results_cleaned.csv"

cut_sheet_filename = "real_data/cut_sheet.csv"
cut_sheet_2_filename = ""

rush_profile_filename = "real_data/rush_profile_cleaned.csv"

summary_filename = "real_data/survey_summary.csv"
# ==============================================================================================

score_filenames = [sd_scores_filename, mingle_scores_filename, gn_scores_filename]
rushes = []

# rush profile data
with open(rush_profile_filename, newline="") as f:
    reader = csv.reader(f)
    data = list(reader)

for row in data[1:]:
    new_rush = Rush(row[1].lower(), row[2].lower())
    new_rush.major = row[5]
    new_rush.year = row[8]
    new_rush.previously_knowns = row[9]
    new_rush.clubs = row[10]
    new_rush.gpa = row[11]
    new_rush.email = row[3]
    rushes.append(new_rush)

# event data
for i in range(3):
    # get csv of scores from an event
    with open(score_filenames[i], newline="") as f:
        reader = csv.reader(f)
        data = list(reader)
    # add scores to local data
    for row in data[1:]:
        found = False
        if row[1].lower() == 'rkb5693':
            print('looking')
        for rush in rushes:
            if rush.id == row[1].lower():
                if row[1].lower() == 'rkb5693':
                    print('found')
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
        if not found:
            print('not found', row[1].lower())
            new_rush = Rush(row[0], row[1].lower())
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
    for i in range(3):
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
if cut_sheet_2_filename:
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

rushes.sort(key=lambda r: r.db_score, reverse=True)
# write score breakdown
with open(summary_filename, "w") as csvfile:
    csv_writer = csv.writer(csvfile)
    csv_writer.writerow(
        [
            "Name",
            "id",
            "Overall Score",
            "Speed Dating Score",
            "Speed Dating Interactions",
            "Mingle Score",
            "Mingle Interactions",
            "Game Night Score",
            "Game Night Interactions",
            "Year",
            "email"
        ]
    )
    for rush in rushes:
        if not rush.cut:
            csv_writer.writerow(
                [
                    rush.name,
                    rush.id,
                    round(rush.db_score, 3),
                    round(rush.scores[0], 3),
                    rush.interactions[0],
                    round(rush.scores[1], 3),
                    rush.interactions[1],
                    round(rush.scores[2], 3),
                    rush.interactions[2],
                    rush.year,
                    rush.email
                ]
            )
