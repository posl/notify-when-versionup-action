import sys, re
from func import (
    split_grep_result, is_issue_closed, is_new_version_released,
    edit_code, revert_code,
    get_issue_pr_message, get_release_pr_message
)
from git import GitClass

def main():
    git_token = sys.argv[1]
    git_owner_repo = sys.argv[2].split("/")
    # ↓ ex) refs/heads/main -> ['refs/heads/main', 'main]
    default_branch = re.search(r'refs/heads/(.*)', sys.argv[3])[1]
    target_type = sys.argv[4]

    file_path, line, target_info = split_grep_result(target_type, sys.argv[5])
    print(file_path, line, target_info)
    

    """
    notify の条件確認
    """
    if target_type == "issue":
        response = is_issue_closed(owner=target_info[0], repo=target_info[1], number=target_info[2])
        if not response:
            print("this issue is 'still opened' or 'closed at more than a day ago'.")
            return
    else:
        response = is_new_version_released(owner=target_info[0], repo=target_info[1])
        if not response:
            print("new version is 'not released' or 'released at more than a day ago'.")
            return


    """
    修正できる箇所に コメント '# this may be fixed!' を挿入する
    """
    edit_code(file_path=file_path, line=line)

    """
    Git: ブランチ作成 / コミット作成 / PR作成
    """
    git = GitClass(owner=git_owner_repo[0], repo=git_owner_repo[1], base_branch=default_branch, git_token=git_token)

    try:
        print("start GitAction")
        base_sha = git.GetBaseSha()
        print("done GetBaseSha")
        git.CreateBranch(base_sha=base_sha)
        print("done CreateBranch")
        content_sha = git.GetContentSha(file_path=file_path)
        print("done GetContentSha")
        git.PushToGitHub(file_path=file_path, content_sha=content_sha)
        print("done PushToGitHub")
        if target_type == "issue":
            message = get_issue_pr_message(issue=response)
        else:
            message = get_release_pr_message(release=response)
        print("done GetPullRequest Docs")
        git.CreatePullRequest(message=message)
        print("done CreatePullRequest")
    except Exception:
        print('Faild...')

    """
    挿入したコメント '# this may be fixed!' を削除する
    """
    revert_code(file_path=file_path, line=line)

    print("Done! notifyAction")

if __name__ == "__main__":
    print("hello, world in python")
    main()
