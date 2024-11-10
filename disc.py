def calculate_max_fusions(timber, tender, abidos):
    # Check for invalid inputs
    if not all(isinstance(x, int) for x in [timber, tender, abidos]):
        return "cant make any"
    
    # Check for negative values or too low to perform any fusion
    if any(x < 0 for x in [timber, tender, abidos]):
        return "cant make any"
    
    # Constants for resource requirements
    TIMBER_PER_FUSION = 86
    TENDER_PER_FUSION = 45
    ABIDOS_PER_FUSION = 33
    
    if timber < TIMBER_PER_FUSION and tender < TENDER_PER_FUSION and abidos < ABIDOS_PER_FUSION:
        return "cant make any"
    
    # Constants for conversion rates
    TIMBER_TO_LUMBER = 80  
    TENDER_TO_LUMBER = 80  
    LUMBER_TO_ABIDOS = 10  
    
    best_result = {
        'max_fusions': 0,
        'timber_to_convert': 0,
        'tender_to_convert': 0,
        'remaining_timber': timber,
        'remaining_tender': tender,
        'remaining_abidos': abidos
    }
    
    try:
        max_timber_conversions = min(timber // 100, (2**31 - 1) // TIMBER_TO_LUMBER)
        max_tender_conversions = min(tender // 50, (2**31 - 1) // TENDER_TO_LUMBER)
        
        for timber_conversions in range(max_timber_conversions + 1):
            remaining_timber = timber - (timber_conversions * 100)
            lumber_from_timber = timber_conversions * TIMBER_TO_LUMBER
            
            for tender_conversions in range(max_tender_conversions + 1):
                remaining_tender = tender - (tender_conversions * 50)
                lumber_from_tender = tender_conversions * TENDER_TO_LUMBER
                
                total_lumber = lumber_from_timber + lumber_from_tender
                
                if total_lumber >= 100: 
                    new_abidos = (total_lumber // 100) * LUMBER_TO_ABIDOS
                else:
                    new_abidos = 0

                total_abidos = abidos + new_abidos

                possible_fusions_timber = remaining_timber // TIMBER_PER_FUSION
                possible_fusions_tender = remaining_tender // TENDER_PER_FUSION
                possible_fusions_abidos = total_abidos // ABIDOS_PER_FUSION

                fusions = min(possible_fusions_timber, possible_fusions_tender, possible_fusions_abidos)

                if fusions > best_result['max_fusions']:
                    best_result = {
                        'max_fusions': fusions,
                        'timber_to_convert': timber_conversions * 100,
                        'tender_to_convert': tender_conversions * 50,
                        'remaining_timber': remaining_timber - (fusions * TIMBER_PER_FUSION),
                        'remaining_tender': remaining_tender - (fusions * TENDER_PER_FUSION),
                        'remaining_abidos': total_abidos - (fusions * ABIDOS_PER_FUSION),
                        'lumber_powder_created': total_lumber,
                        'new_abidos_from_conversion': new_abidos
                    }
                    
            if best_result['max_fusions'] > 0 and remaining_timber < TIMBER_PER_FUSION:
                break

        return best_result

    except (OverflowError, ValueError):
        return "cant make any"
