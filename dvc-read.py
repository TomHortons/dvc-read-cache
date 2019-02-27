from git import Repo
import os


class DvcHub(object):
    def fileNameToMD5(self, dvcFile):
        parsed = dvcFile.split('\n')
        outputs = parsed[parsed.index('outs:')+1:]

        startPoints = [i for i, x in enumerate(list(map(lambda x: x[:2] == '- ', outputs))) if x]
        out_list = []
        for n in range(len(startPoints)):
            dict_ = {}
            if n == len(startPoints) - 1:
                output = outputs[startPoints[n]:]
            else:
                output = outputs[startPoints[n]:startPoints[n+1]]
            output = list(map(lambda x: x[2:], output))
            for param in output:
                tmp = param.split(': ')
                dict_[tmp[0]] = tmp[1]
            out_list.append(dict_)

        dummy = []
        for i in out_list:
            dummy.append({
                'name': i['path'],
                'md5': i['md5']
            })
        if len(dummy) == 0:
            return None
        return dummy

    def dvchub(self, branch_tag, f_name, repo, out=0):
        dvc_file = repo.git.show('{}:{}'.format(branch_tag, f_name))
        md5s = self.fileNameToMD5(dvc_file)
        
        root_path = repo.git.rev_parse("--show-toplevel")
        md5 = md5s[out]['md5']
        path_to_file = os.path.join(root_path, '.dvc/cache', md5[:2], md5[2:])
        return md5s[out]['name'], path_to_file
        

repo = Repo('/Users/tomoya/VSCode/mail-models/')
fname, pathToFile = dvchub('v-0.7', 'analysis/nerDF.csv.dvc', repo)