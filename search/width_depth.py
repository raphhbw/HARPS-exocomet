def left(index, arr):
    
    count = 0
    l_arr = arr[:index]
    # print(l_arr.shape)
    
    if len(l_arr) > 1:
        for i in range(1, len(l_arr)+1):
            # print('went through1')
            # print(i)
            # print(arr[index - i])
            if arr[index - i] <= -3:
                count += 1
            else:
                return count
            
    elif len(l_arr) ==1:
        # print('went through2')
        if arr[index - 1] <= -3:
            count += 1
        # return count
        
    # else:
        # print('went through3')
    return count

def right(index, arr):
    
    count = 0
    l_arr = arr[index+1:]
    # print(l_arr.shape)
    
    if len(l_arr) > 1:
        # print('went through1')
        for i in range(1, len(l_arr)+1):
            # print('index: ',i)
            if arr[index + i] <= -3:
                # print('index: ',i)
                count += 1
            else:
                return count
            
    elif len(l_arr) ==1:
        # print('went through2')
        if arr[index + 1] <= -3:
            count += 1
        # return count      
    
    # else:
        # print('went through3')
    return count