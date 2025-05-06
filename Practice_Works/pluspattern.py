def find_all_plus_signs(matrix):
    if not matrix or len(matrix) < 3 or len(matrix[0]) < 3:
        return []
    
    rows = len(matrix)
    cols = len(matrix[0])
    plus_signs = []
    
    for i in range(rows):
        for j in range(cols):
            max_arm = min(i, rows - 1 - i, j, cols - 1 - j)
            
            for arm in range(1, max_arm + 1):
                # Check if all four directions have valid indices
                if (i - arm >= 0 and i + arm < rows and
                    j - arm >= 0 and j + arm < cols):
                    # Collect elements
                    center = matrix[i][j]
                    up = matrix[i - arm][j]
                    down = matrix[i + arm][j]
                    left = matrix[i][j - arm]
                    right = matrix[i][j + arm]
                    
                    elements = [center, up, down, left, right]
                    total = sum(elements)
                    
                    plus_signs.append({
                        'center': (i, j),
                        'arm_length': arm,
                        'elements': elements,
                        'sum': total
                    })
                else:
                    break  # No larger arm possible
    
    return plus_signs

# Example usage:
matrix = [
    [1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10],
    [11, 12, 13, 14, 15],
    [16, 17, 18, 19, 20],
    [21, 22, 23, 24, 25]
]

plus_signs = find_all_plus_signs(matrix)
for sign in plus_signs:
    print(f"Plus at center {sign['center']} with arm length {sign['arm_length']}:")
    print(f"  Elements: {sign['elements']}")
    print(f"  Sum: {sign['sum']}\n")