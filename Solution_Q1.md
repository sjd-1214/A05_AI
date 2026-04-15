# Question 1: The Zoo in Killian Court

## Part 1

### 1) Define the CSP
**Variables:**
- LION (L)
- ANTELOPE (A)
- HYENA (H)
- EVIL LION (EL)
- HORNBILL (HB)
- MEERKAT (M)
- BOAR (B)

**Initial Reduced Domains (after applying unary constraint LION=1):**
- LION: {1}
- ANTELOPE: {1, 2, 3, 4}
- HYENA: {1, 2, 3, 4}
- EVIL LION: {1, 2, 3, 4}
- HORNBILL: {1, 2, 3, 4}
- MEERKAT: {1, 2, 3, 4}
- BOAR: {1, 2, 3, 4}

*Note: Adjacencies in layout: (1,2), (2,3), (3,4).*

### 2) Constraint Graph
Nodes: {L, A, H, EL, HB, M, B}
Edges (Constraints):
- (L, EL): L != EL
- (M, B): M == B
- (H, L), (H, A), (H, HB), (H, M), (H, B): H != others (except EL)
- (EL, M), (EL, B), (EL, HB): EL != diet animals
- (L, A): A != L AND A not adjacent to L (if L=1, A cannot be 1 or 2)
- (EL, A): A != EL AND A not adjacent to EL
- (L, HB): HB != L

## Part 2

### 1) Solving with DFS + Forward Checking + Propagation

**Step 1: Assign LION = 1**
- Queue for propagation: [A, EL, H, HB] (Neighbors of LION affected by assignment)
- **Process A:** L=1 implies A != 1 and A != 2. A domain: {3, 4}.
- **Process EL:** L=1 implies EL != 1. EL domain: {2, 3, 4}.
- **Process H:** L=1 implies H != 1. H domain: {2, 3, 4}.
- **Process HB:** L=1 implies HB != 1. HB domain: {2, 3, 4}.
- Domains after LION=1:
  - L: {1}, A: {3, 4}, EL: {2, 3, 4}, H: {2, 3, 4}, HB: {2, 3, 4}, M: {1, 2, 3, 4}, B: {1, 2, 3, 4}

**Step 2: Assign HORNBILL = 2 (Tie-break: alphabetical L->A->B->EL->HB... Wait, instructions say break ties in numerical order for values, and alphabetical for queue. Let's pick next variable: ANTELOPE)**
- **Assign ANTELOPE = 3**
- Queue: [EL] (A=3 implies EL != 3 and EL not adjacent to 3, so EL != 2, 3, 4? No, EL not adjacent to A means if A=3, EL cannot be 2 or 4. EL != 3 anyway).
- **Process EL:** A=3. EL cannot be 3. EL cannot be 2 or 4 (adjacent). EL domain becomes empty? 
- *Correction on ANTELOPE constraint:* "ANTELOPE cannot be in either the same enclosure or in an enclosure adjacent to the LION or EVIL LION."
  - This means if EL is in enclosure X, A cannot be in X or adjacent to X.
  - Current Domains: L:{1}, A:{3,4}, EL:{2,3,4}, H:{2,3,4}, HB:{2,3,4}, M:{1,2,3,4}, B:{1,2,3,4}
  - Since L=1, A must be in {3, 4} (not 1 or 2).
  - If we pick **EL = 4**:
    - A cannot be 4 or 3. A domain becomes empty. (Backtrack)
  - If we pick **EL = 2**:
    - A cannot be 2 or 1 or 3. A domain: {4}.
    - Queue for EL=2: [A, H, HB, M, B]
    - **Process A:** EL=2. A cannot be 1, 2, 3. A domain: {4}.
    - **Process H:** H can share with EL. So H=2 is okay. But H smells bad... "Only the EVIL LION will share his enclosure." This means if H is in 2, no one else but EL can be in 2.
    - **Process HB:** EL=2 implies HB != 2. HB domain: {3, 4}.
    - **Process M:** EL=2 implies M != 2. M domain: {1, 3, 4}.
    - **Process B:** EL=2 implies B != 2. B domain: {1, 3, 4}.

**Current State:** L:1, EL:2, A:4.
- Remaining: H, HB, M, B.
- **Assign HYENA = 2** (Sharing with EL)
  - Queue: [HB, M, B]
  - H=2. No one else can be in 2. (Already satisfied by EL constraint?)
- **Assign HORNBILL = 3**
- **Assign MEERKAT = 4**
- **Assign BOAR = 4** (M==B)

**Final Solution Found:**
- LION: 1
- ANTELOPE: 4
- HYENA: 2
- EVIL LION: 2
- HORNBILL: 3
- MEERKAT: 4
- BOAR: 4

### Domain Worksheet Trace (Simplified)
| Step | Var Assigned | Values Eliminated | Backtrack? |
|------|--------------|-------------------|------------|
| 1    | LION = 1     | A: 1,2; EL: 1; H: 1; HB: 1 | No |
| 2    | ANTELOPE = 3 | EL: 2,3,4 (EL cannot be adj to A=3) | Yes |
| 3    | ANTELOPE = 4 | EL: 3,4 (EL cannot be adj to A=4) | No |
| 4    | EVIL LION = 2| H: 1,3,4 (H must be with EL? No, H can be alone or with EL); A already 4. | No |
| ...  | ...          | ...               | ...        |

## Search Tree
```
       LION=1
         |
    ANTELOPE=4
         |
    EVIL LION=2
      /      \
   HYENA=2  ...
     |
  HORNBILL=3
     |
  MEERKAT=4
     |
   BOAR=4
```

*(Note: The above is a summary. Full worksheet would follow the table format provided in the PDF.)*
