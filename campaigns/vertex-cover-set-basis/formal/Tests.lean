import Challenge
open VertexCoverSetBasis
example : targetWitness ⟨3, [[0,1],[1,2]], 2⟩ [[0,1],[1,2]] = true := by native_decide
example : targetWitness ⟨3, [[0,1],[1,2]], 1⟩ [[0,1,2]] = false := by native_decide
