# read input
input = open(joinpath(@__DIR__, "input", "input.txt")) do f
    readlines(f)
end

shape_names_dict = Dict{String, String}(
    "A" => "rock",
    "B" => "paper",
    "C" => "scissors",
    "X" => "rock",
    "Y" => "paper",
    "Z" => "scissors",
)

# Schema: (elves play, you play) => outcome
shape_vs_dict = Dict{Tuple{String, String}, String}(
    ("A", "X") => "draw",
    ("A", "Y") => "win",
    ("A", "Z") => "loss",
    ("B", "X") => "loss",
    ("B", "Y") => "draw",
    ("B", "Z") => "win",
    ("C", "X") => "win",
    ("C", "Y") => "loss",
    ("C", "Z") => "draw"
)

shape_names_dict_pt2 = Dict{String, String}(
    "X" => "loss",
    "Y" => "draw",
    "Z" => "win",
)

# Schema (elves play, result should be) => you play
shape_vs_dict_pt2 = Dict{Tuple{String, String}, String}(
    ("A", "draw") => "X",
    ("A", "win") => "Y",
    ("A", "loss") => "Z",
    ("B", "loss") => "X",
    ("B", "draw") => "Y",
    ("B", "win") => "Z",
    ("C", "win") => "X",
    ("C", "loss") => "Y",
    ("C", "draw") => "Z"
)


point_dict = Dict{String, Int64}(
    "X" => 1,
    "Y" => 2,
    "Z" => 3,
    "draw" => 3,
    "loss" => 0,
    "win"  => 6
)



# Part 1
function part1(input)
    scores = []
    for line in input
        elves, you = split(line, " ")
        outcome = shape_vs_dict[(elves, you)]
        score = (point_dict[you] + point_dict[outcome])
        println("Elves: $(shape_names_dict[elves]), You: $(shape_names_dict[you]), Outcome: $(outcome), Score: $score")
        push!(scores, score)
    end
    return sum(scores)
end

# Part 2
function part2(input)
    scores = []
    for line in input
        elves, outcome = split(line, " ")
        you = shape_vs_dict_pt2[(elves, shape_names_dict_pt2[outcome])]
        push!(scores, (point_dict[you] + point_dict[shape_names_dict_pt2[outcome]])) 
    end
    return sum(scores)
end


res = part1(input)
println("Part 1: $res")

res2 = part2(input)
println("Part 2: $res2")