import csv

class InterviewWeighter:
    def __init__(self, interview_results_filename):
        self.interviewers = {}  # Dictionary to store interviewer scores
        self.global_sum = 0  # Sum of all interview scores
        self.global_count = 0  # Total number of interview scores
        self.interview_results_filename = interview_results_filename  # Store the filename

    def process_interviews(self):
        with open(self.interview_results_filename, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header row

            for row in csv_reader:
                interviewer = row[2]
                score = float(row[3])
                interviewee = row[0]

                # Update global sum and count
                self.global_sum += score
                self.global_count += 1

                # Update interviewer's score
                if interviewer in self.interviewers:
                    self.interviewers[interviewer].append(score)
                else:
                    self.interviewers[interviewer] = [score]

        # Calculate the global average
        global_avg = self.global_sum / self.global_count

        # Calculate the average for each specific interviewer and subtract the global average
        interviewer_avg_diff = {}
        for interviewer, scores in self.interviewers.items():
            avg = sum(scores) / len(scores)
            avg_diff = avg - global_avg
            interviewer_avg_diff[interviewer] = avg_diff

        return interviewer_avg_diff


# CHANGE THESE =================================================================================
interview_results_filename = "old_data/fall2022interviews.csv" # Provide the correct path to the CSV file
# ==============================================================================================

# Create an instance of the InterviewWeighter class and process the interviews
weighter = InterviewWeighter(interview_results_filename)
interviewer_avg_diff = weighter.process_interviews()

# Print the interviewer average differences
for interviewer, avg_diff in interviewer_avg_diff.items():
    print(f"Interviewer: {interviewer}, Average Difference: {avg_diff}")
