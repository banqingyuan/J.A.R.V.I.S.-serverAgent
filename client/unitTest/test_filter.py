import biz.action_filter

def test_action_filter():
    biz.action_filter.action_music("告白气球.mp3")


if __name__ == "__main__":
    test_action_filter()


    # # 根据正则匹配[]中的内容
    # action = re.findall(r"\[(.*?)\]", msg_with_action)
    # if len(action) == 0:
    #     return msg_with_action
    #
    # # 删除[]以及其中的内容
    # msg = re.sub(r"\[(.*?)\]", "", msg_with_action)
    # return msg