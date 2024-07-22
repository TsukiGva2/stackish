import forth.instruction as InstructionTypes


def forth_type_to_string(t):
    match t.lower():
        case "word":
            return InstructionTypes.Word
        case "label":
            return InstructionTypes.Label
        case "instruction":
            return InstructionTypes.Instruction
