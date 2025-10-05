# Sprint 1 Report (August 18, 2025 - October 10, 2025)

## YouTube link of Sprint 1 Video

TODO: RECORD VIDEO

## What's New (User Facing)

- Language Model (Gemini currently) to communicate with for tutoring session
- Web-based GUI
- Quiz system for tutor to provide feedback for the student

## Work Summary (Developer Facing)

We began our research into using LLMs for tutoring purposes. We did experimentation and research into prompt engineering, which allowed us to come up with a strong initialization prompt for the LLM to be able to properly have safeguards and avoid security or privacy issues. We also made use of JSON formatting for the LLM's responses for the quiz system, which will help with making the quiz system more friendly on the user-facing side.

## Unfinished Work

- Capability for school administrators to view usage reports
- Creating system for teachers to monitor and track student progress in learning
- System for teacher to be alerted if a student is struggling to learn
- Using a local-LLM rather than a cloud-hosted one like Gemini, for use on a school district server

## Completed Issues/User Stories

Here are links to the issues that we completed in this sprint:

- URL of issue 1
- URL of issue 2
- URL of issue n

Reminders (Remove this section when you save the file):

- Each issue should be assigned to a milestone
- Each completed issue should be assigned to a pull request
- Each completed pull request should include a link to a "Before and After" video
- All team members who contributed to the issue should be assigned to it on GitHub
- Each issue should be assigned story points using a label
- Story points contribution of each team member should be indicated in a comment

## Incomplete Issues/User Stories

Here are links to issues we worked on but did not complete in this sprint:

- URL of issue 1 <<One sentence explanation of why issue was not completed>>
- URL of issue 2 <<One sentence explanation of why issue was not completed>>
- URL of issue n <<One sentence explanation of why issue was not completed>>

Examples of explanations (Remove this section when you save the file):

- "We ran into a complication we did not anticipate (explain briefly)."
- "We decided that the feature did not add sufficient value for us to work on it in this sprint (explain briefly)."
- "We could not reproduce the bug" (explain briefly).
- "We did not get to this issue because..." (explain briefly)

## Code Files for Review

Please review the following code files, which were actively developed during this sprint, for quality:

- [Name of code file 1](https://github.com/your_repo/file_extension)
- [Name of code file 2](https://github.com/your_repo/file_extension)
- [Name of code file 3](https://github.com/your_repo/file_extension)

## Retrospective Summary

Here's what went well:

- Research into prompt engineering
- Usage of JSON and CSV for quiz system
- Connection to LLM via API
- Creation of web app UI

Here's what we'd like to improve:

- Roles and account system
- Connection to a local LLM rather than to Gemini's cloud-based LLM

Here are changes we plan to implement in the next sprint:

- Usage of local LLM for school district server
- Teacher intervention notifications
- Role-based access for teachers, admins and students
- Progress dashboard w/ exports
