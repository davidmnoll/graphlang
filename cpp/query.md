
The syntax should be something like the following: 

```


# would fail typecheck because it's not in an IO function
# mydb <= bool

export: 
  mydb:
    - bool




# this selects any functions matchign the type bbf with teh where predicate

and <= bbf from mydb where 
  & (true -> true -> true) 
  & (true -> false -> false) 
  & (true -> false -> false)
  & (false -> true -> false)

and 





not : bool -> bool
| true = false
| false = true 

bbf = bool -> bool -> bool 



# if this were instead 
Bool = T | F
# both true | false annd T | F would resolve to the same CID
# T F and Bool would each be aliases that also point to the same CIDs as
# true, false and bool respectively



bool : [true, false]


import : 

  : &mydb
  # file
  ///.mydb : &mydb1
  # the following uses http connection w/ rest API
  https://localhost:3333/mydb : &mydb2
  # uses git
  git://localhost:3333/mydb : &mydb3
  # jdbc
  jdbc://user:pass@host:port/mydb : &mydb4


```

This should parse into a tree like the following 


