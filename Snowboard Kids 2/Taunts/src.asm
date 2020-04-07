addr:
8003A0FC
J $80380020
addr:
80380020
# Store return address:
LUI T0, $8038
SW RA, $0000(T0)

# ============================:
CheckControllers:
# ============================:
LUI T1, $800A
ADDI T1, T1, $1C02
ADDI T2, T0, $0000
LUI T6, $8026
ADDI T6, T6, $90D8
JAL CheckController
NOP
JAL CheckController
NOP
JAL CheckController
NOP
JAL CheckController
NOP
J ReloadReturn

DecrementCooldown:
ADDI T5, T5, $FFFF
SH T5, $0002(T2)
J Backup
NOP


# ============================:
CheckController:
# ============================:
# Move our pointers:
ADDI T1, T1, $0006
ADDI T2, T2, $0004
ADDI T6, T6, $0001

# Load their values:
LH T3, $0000(T1)
LH T4, $0000(T2)
LH T5, $0002(T2)

BNEZ T5, DecrementCooldown
NOP

# Has input changed? :
BNE T3, T4, GetSound
NOP

# Store new backup:
Backup:
SH T3, $0000(T2)
JR RA
NOP

GetSound:
LB T7, $0000(T6)
LUI T8, $8038
ADDI T8, T8, $1000
ADDI T9, R0, $0010
MULT T7, T9
MFLO T7
ADD T8, T8, T7
ADDI T8, T8, $FFFE

# Right on D-Pad:
ADDI T7, R0, $0100
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# Left on D-Pad:
ADDI T7, R0, $0200
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# Down on D-Pad:
ADDI T7, R0, $0400
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# Up on D-Pad:
ADDI T7, R0, $0800
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# L+Right on D-Pad:
ADDI T7, R0, $0120
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# L+Left on D-Pad:
ADDI T7, R0, $0220
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# L+Down on D-Pad:
ADDI T7, R0, $0420
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# L+Up on D-Pad:
ADDI T7, R0, $0820
BEQ T3, T7, PlaySound
ADDI T8, T8, $0002

# Nothing...:
J Backup

# ============================:
PlaySound:
# ============================:
# Apply a cooldown:
LHU T5, $0014(T0)
SH T5, $0002(T2)

LHU A0, $0000(T8)
JAL $800585C8
SH T3, $0000(T2)
J ReloadReturn

# ================= Exit Point:
ReloadReturn:
LUI T0, $8038
LW RA, $0000(T0)
J $8003A1D0
NOP
