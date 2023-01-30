def exceptions(name):
    
    # Case for BD catalogue
    if name[0:2] == 'BD':
        return name
    
    # Case for ex. CD-234-2432
    if name[0:2] == 'CD':
        rest_name = name[3:]
        #print(rest_name)
        #if rest_name.contains('-'):
        if '-' in rest_name:
            rest_name = rest_name.replace('-', '')
        name = name[0:3] + rest_name
        #print(name)
        return name
    
    # Case for J###-##
    if (((name[1].isnumeric()) == True) & (name[0] == 'J')):
        return name
    
    # Case for G##-##
    if (((name[1].isnumeric()) == True) & (name[0] == 'G')):
        return name
    
    # Case for CPD-###
    if name[0:3] == 'CPD':
        return name
    
    # Case for LP catalogue
    if len(name)>3:
        if (((name[2].isnumeric()) == True) & (name[0:2] == 'LP')):
            return name
    
    # Case for SERAM catalogue??
    if len(name)>5: # if name smaller will create issues with this condition
        if name[0:5] == 'SERAM':
            beg_name = name[:7]
            if '-' in beg_name:
                name = beg_name.replace('-','') + name[7:]
            
            return name
    
    # Case of SW catalogue
    if name[0:2] == 'SW':
        return name
            
    # Case for TYC catalogue
    if name[0:3] == 'TYC':
        beg_name = name[:5]
        # print(beg_name)
        if '-' in beg_name:
            name = beg_name.replace('-','') + name[5:]

        return name
    
    return name.replace('-', ' ')

def to_reduce(star):
    san = exceptions(star)
    san = san.replace('_', ' ')
    red = san.lower()
    red = red.replace(' ', '')
    return red