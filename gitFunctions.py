from pydriller import RepositoryMining
import csv
import time
from neo4jrestclient.client import GraphDatabase


def initialise():
    file_shared_by = {}
    committer_set = set()
    db = GraphDatabase("http://localhost:7474", username="neo4j",
                       password="n3o4j")
    committer_email = db.labels.create("CommitterEmail")
    for commit in RepositoryMining(
            '/Users/kirtanasuresh/Documents/WebDev/myapp/che',
            only_in_branch="master").traverse_commits():

        # prevent duplicate node creation
        if commit.committer.email == "noreply@github.com":
            email = commit.author.email
        else:
            email = commit.committer.email
        # name = commit.committer.name
        if email not in committer_set:
            committer_set.add(email)
            committer_email.add(db.nodes.create(name=email))

        for mod in commit.modifications:
            if mod.filename in file_shared_by:
                file_shared_by[mod.filename].add(email)
            else:
                com = set()
                com.add(email)
                file_shared_by[mod.filename] = com


    # file_shared_by['pink'] = {'purple', 'magenta'}
    # file_shared_by['orange'] = {'red', 'yellow'}
    print("mapping complete")
    with open('filemap.csv', 'w') as f:
        w = csv.writer(f, delimiter=',')
        for key, values in file_shared_by.items():
            values = ' '.join(values)
            w.writerow([key, values])


def main():
    start_time = time.time()
    initialise()
    print("--- %s seconds to map the file ---" % (time.time() -
                                                   start_time))


if __name__ == '__main__':
    main()