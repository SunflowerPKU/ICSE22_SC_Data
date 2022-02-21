import datetime
import mysql.connector
with open('tensorflow_nodes_time', 'w') as of:
    of.write('id' + ',' + 'label' + ',' + 'start_time' + ',' + 'end_time' + '\n')
    cnx = mysql.connector.connect(user='ubuntu', password='OSSLab@123', database='libraries')
    with open('tensorflow_nodes') as f:
        next(f)
        for line in f:
            id, name = line.strip('\n').split(',')
            repo_name = name.split(' ')[0]
            repo = 'https://github.com/' + repo_name.replace('_', '/')
            query = ("SELECT repository_url, created_timestamp  FROM projects WHERE platform = 'Pypi' and repository_url = '%s'"%(repo))
            curA = cnx.cursor(buffered=True)
            curA.execute(query)
            rows_count = curA.rowcount
            if rows_count > 0:
                for repository_url, created_timestamp in curA:
                    of.write(id + ',' + repo_name + ',' + created_timestamp.strftime('%Y-%m-%d %H:%M:%SZ') + ',' + '2020-01-30 00:00:00' + '\n')
                    break
            else:
                print(id, repo_name)
                of.write(id + ',' + repo_name + ',' + '2015-12-01 00:00:00' + ',' + '2020-01-30 00:00:00' + '\n')