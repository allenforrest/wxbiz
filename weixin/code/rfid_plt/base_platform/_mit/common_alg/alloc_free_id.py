#coding=gbk

def alloc_free_id(moc_db_contain, attr_name, min_value, max_value):
    cur_max_value = moc_db_contain.get_attr_max_value(attr_name)
    ret_value = min_value
    
    if cur_max_value is None:
        ret_value = min_value
    elif cur_max_value >= max_value:
        ret_value = min_value
        
        # 查找空闲的
        values_in_db = moc_db_contain.lookup_attrs([attr_name])
        values_in_db.sort()
        
        for tmp_value in values_in_db:
            tmp_value = tmp_value[0]
            if ret_value < tmp_value:
                break
            elif ret_value == tmp_value:
                imc_id += 1
            else:
                continue
            
        if ret_value > max_value:
            ret_value = None
            
    else:
        ret_value = cur_max_value + 1        
        
    return ret_value

