from string import Template

MAIN_HTML = Template("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>releventRooms</title>
    <style>
        body {
        margin: 10%;
        font-family: "IBM Plex Mono"
        }
  
        img {
        width: 45%;
        }
    </style>
</head>
<body>
<h1>hot words: ${hotwords}</h1>

<form action = "http://localhost:5000/" method = "post">
    <p>Please input several search words:</p>
    <p><input type = "text" name = "search_words" /></p>
    <p><input type = "submit" value = "submit" /></p>
 </form>

${images}

</body>
</html
""")

def images_html(hotwords, urls):

    images = Template(
        """
        <img src="${source1}" alt="Italian Trulli">
        <img src="${source2}" alt="Italian Trulli">
        <img src="${source3}" alt="Italian Trulli">
        <img src="${source4}" alt="Italian Trulli">
        <img src="${source5}" alt="Italian Trulli">
        <img src="${source6}" alt="Italian Trulli">
        <img src="${source7}" alt="Italian Trulli">
        <img src="${source8}" alt="Italian Trulli">
        <img src="${source9}" alt="Italian Trulli">
        <img src="${source10}" alt="Italian Trulli">
        """)
    
    images = images.safe_substitute({"source1":urls[0],
                       "source2":urls[1],
                       "source3":urls[2],
                       "source4":urls[3],
                       "source5":urls[4],
                       "source6":urls[5],
                       "source7":urls[6],
                       "source8":urls[7],
                       "source9":urls[8],
                       "source10":urls[9]})
    
    h = MAIN_HTML.substitute(hotwords=hotwords, images=images)
    return h