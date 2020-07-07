# Scripts
Useful scripts that maybe beneficial to the research group.

Please make sure scripts that are not for specific DFT codes are placed in the General folder with a short description of how it is used. This maybe in the form of a readme file or as comments in the script itself.

If your script is for a specific DFT code that does not have a folder please make a new folder for it.

Steps to set up Git on your local machine:

1: To add scripts to the repository download a program that allows you to clone, push and pull to the git repository such as 'git bash' download from: https://gitforwindows.org/

2: You will need to set up an SSH key so you can connect locally (this is quite easy using git bash): https://help.github.com/en/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

3: Then add the SSH key to your git profile: https://help.github.com/en/github/authenticating-to-github/adding-a-new-ssh-key-to-your-github-account

4: Once your account is set up you can save your user name and email address in git bash using the following command:
    git config --global user.name "Your Name"
    git config --global user.email you@example.com


4: You will need to 'clone' the scripts repository to your local machine saves the repository as a file which you can sync with the remote repository this can be done with the following command:
    git clone ssh/https
    
5: Once you have cloned the repository you can add your own scripts to the master branch by copying them into your local git directory and putting them into the appropiate folder/s (if a folder does not exists then you can make a new one).

6: To add the new files to the remote repository via git bash use the following commands:
    git add .
    git commit -m "your message goes here"
    git push origin master
    
7: Login to GitHub and make sure the files were correctly pushed to the repository.

8: To get any new files from the repository use the following command (make sure you change the directory to your local git repository file):
    git pull origin master
    





