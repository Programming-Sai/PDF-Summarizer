

OG = "The Boy is a Speedster"
sub_OG = "Boy is"

i = OG.find(sub_OG)
j = OG.find(sub_OG)+len(sub_OG)

print(i, j, OG[i:j], OG.replace(OG[i:j], ""), OG)