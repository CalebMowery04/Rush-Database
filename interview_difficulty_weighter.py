import csv

class InterviewWeighter:
    def __init__(self, interview_results_filename):
        self.interviewers = {}
        self.global_sum = 0
        self.global_count = 0
        self.interview_results_filename = interview_results_filename

    def process_interviews(self):
        processed_rows = []  # Store the processed rows
        with open(self.interview_results_filename, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)

            for row in csv_reader:
                interviewer = row[2]
                score = float(row[3])

                self.global_sum += score
                self.global_count += 1

                if interviewer in self.interviewers:
                    self.interviewers[interviewer].append(score)
                else:
                    self.interviewers[interviewer] = [score]

                processed_rows.append(row)

        global_avg = self.global_sum / self.global_count

        interviewer_avg_diff = {}
        for interviewer, scores in self.interviewers.items():
            avg = sum(scores) / len(scores)
            avg_diff = avg - global_avg
            interviewer_avg_diff[interviewer] = avg_diff

        adjusted_rows = []
        for row in processed_rows:
            score = float(row[3])
            interviewer = row[2]
            adjusted_score = round((score - interviewer_avg_diff[interviewer])*2)/2
            row.append(adjusted_score)
            adjusted_rows.append(row)

        new_filename = "adjusted_interview_results.csv"
        with open(new_filename, 'w', newline='') as new_file:
            csv_writer = csv.writer(new_file)
            csv_writer.writerow(header)
            csv_writer.writerows(adjusted_rows)

        return interviewer_avg_diff

# CHANGE THESE =================================================================================
interview_results_filename = "old_data/fall2022interviews.csv"
# ==============================================================================================

weighter = InterviewWeighter(interview_results_filename)
interviewer_avg_diff = weighter.process_interviews()

for interviewer, avg_diff in interviewer_avg_diff.items():
    print(f"Interviewer: {interviewer}, Average Difference: {avg_diff}")
