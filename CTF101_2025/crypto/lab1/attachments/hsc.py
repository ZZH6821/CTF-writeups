from sage.all import *

# Result from the encryption
result = b"\xfc\xf2\x1dE\xf7\xd8\xf7\x1e\xed\xccQ\x8b9:z\xb5\xc7\xca\xea\xcd\xb4b\xdd\xcb\xf2\x939\x0b\xec\xf2"
# Construct the 3x10 RT matrix (row-major: 3 rows, 10 columns)
RT = [[0] * 10 for _ in range(3)]
for j in range(10):
    for i in range(3):
        RT[i][j] = result[j * 3 + i]
allowed_chars = "".join(chr(i) for i in range(32, 127))
allowed_ords = set(ord(c) for c in allowed_chars)
n_allowed = len(allowed_ords)
print(f"Allowed ordinals: {n_allowed}")
# Prepare a list of allowed ordinals for iteration
allowed_ords_list = list(allowed_ords)
# Row sums for MT (from the first column equation)
row_sums = [0] * 3
for i in range(3):
    row_sums[i] = RT[i][0] * pow(65, -1, 256) % 256
# Precomputed RHS for the last column (j=9) equations
rhs3_list = [255, 66, 9]
# Iterate over x, y, p, q. x is FT[0][9], y is FT[1][9], p is FT[1][1], q is FT[2][1]
count = 0
for x in allowed_ords_list:
    for y in allowed_ords_list:
        for p in allowed_ords_list:
            for q in allowed_ords_list:
                count += 1
                if count % 100000 == 0:
                    print(f"Progress: {count} iterations")
                # Build MT row by row
                MT_vals = []
                valid = True
                for i in range(3):
                    # RHS for the second column equation (j=1)
                    if i == 0:
                        rhs2 = (69 - 252 * q) % 256
                    elif i == 1:
                        rhs2 = (247 - 114 * q) % 256
                    else:  # i==2
                        rhs2 = (216 - 221 * q) % 256
                    # Coefficients for the two equations
                    a_val = (123 - q) % 256
                    b_val = (p - q) % 256
                    c_val = (x - 125) % 256
                    d_val = (y - 125) % 256
                    rhs3 = rhs3_list[i]
                    # Check if the 2x2 system is solvable
                    det = (a_val * d_val - b_val * c_val) % 256
                    if gcd(det, 256) != 1:
                        valid = False
                        break
                    # Solve the 2x2 system
                    inv_det = pow(det, -1, 256)
                    a0 = (d_val * rhs2 - b_val * rhs3) * inv_det % 256
                    a1 = (a_val * rhs3 - c_val * rhs2) * inv_det % 256
                    a2 = (row_sums[i] - a0 - a1) % 256
                    MT_vals.append((a0, a1, a2))
                if not valid:
                    continue
                # Construct MT matrix
                MT_mat = matrix(Zmod(256), MT_vals)
                if not MT_mat.is_invertible():
                    continue
                # Compute FT = MT^{-1} * RT
                try:
                    inv_MT = MT_mat.inverse()
                    FT = inv_MT * matrix(Zmod(256), RT)
                except Exception:
                    continue
                # Convert FT to flag string
                flag_chars = []
                for j in range(10):
                    for i in range(3):
                        char_val = int(FT[i, j])
                        if char_val < 0 or char_val > 255:
                            valid = False
                            break
                        flag_chars.append(char_val)
                    if not valid:
                        break
                if not valid:
                    continue
                # Check flag format
                flag_str = "".join(chr(c) for c in flag_chars)
                if (
                    len(flag_str) == 30
                    and flag_str.startswith("AAA{")
                    and flag_str.endswith("}")
                    and all(32 <= ord(c) <= 126 for c in flag_str)
                ):
                    # Check internal characters (positions 4 to 28)
                    internal_valid = True
                    for idx in range(4, 29):
                        if ord(flag_str[idx]) not in allowed_ords:
                            internal_valid = False
                            break
                    if internal_valid:
                        print("Flag found:", flag_str)
                        exit(0)
print("End of search")
