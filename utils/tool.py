def correct_split(text):
    if len(text) > 2000:
        res = []
        max_length = 2000
        words = text.split(" ")
        current = ""
        for word in words:
            if len(current + word + " ") <= max_length:
                current += word + " "
            else:
                res.append(current)
                current = word + " "
        if len(current) > 0:
            res.append(current)
        else:
            res[-1] = res[-1].strip()
        return res
    else:
        return [text]