from cascade import validated_dataclass, field
from cascade.rules import Min

@validated_dataclass
class User:
    id: int
    age: int = field(rules=[Min(18)])

user = User(id=1, age=21)
user.validate()     # passes

user.age = 10
user.validate()     # error and raised RuleValidationError
