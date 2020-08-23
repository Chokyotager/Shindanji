from draw import Shindanji

ji = Shindanji()

img = ji.drawChar([{"radical": "門", "positions": [[1, 3], [1, 3]]},
                    {"radical": "友", "positions": [[1.4, 2.6], [2.5, 2.6]]}],
                    size=500)

img.save("ji.png")
