# Lab 2

**Sierra Layous**

```
#Part 1:
#multiply values in list

part1 = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]
result1 = 1

i=0
while i < len(part1):
    result1 = result1 * part1[i]
    i = i + 1


print('The result of Part 1 is: ',result1)

#Part 2:
#add values in list

part2 = [-1, 23, 483, 8573, -13847, -381569, 1652337, 718522177]
result2 = 0

for i in part2:
    result2 = result2+i

print('The result of Part 2 is: ',result2)

#Part 3:
#add even numbers in list

part3 = [146, 875, 911, 83, 81, 439, 44, 5, 46, 76, 61, 68, 1, 14, 38, 26, 21] 
isEven = i % 2 == 0
result3 = 0

for i in part3:
    if i % 2 == 0:
        result3 = result3 + i

print('The result of Part 3 is: ',result3)

#Prints The result of Part 1 is:  302231454903657293676544
#Prints The result of Part 2 is:  719788176
#Prints The result of Part 3 is:  458
```