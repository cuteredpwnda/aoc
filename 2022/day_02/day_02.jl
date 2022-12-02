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


########### BONUS ###########
## learning some julia here
## define structs
struct Play
    elves::String
    you::String
end

function strPlay(p::Play)::String
    return
        """Elves: $p().elves)
        You: $(p.you)"""
end
struct Result
    outcome::String
    score::Int64
end

function strResult(r::Result)::String
    return
        """Outcome: $(r.outcome)
        Score: $(r.score)"""
end

struct Turn
    play::Play
    result::Result
end

function strTurn(turn::Turn)::String
    playstr = strPlay(turn.play)
    resultstr = strResult(turn.result)
    return """
        $playstr
        $resultstr
        """
end

function play(line, pt2 = false)::Turn
    if pt2
        elves, outcome = split(line, " ")
        you = shape_vs_dict_pt2[(elves, shape_names_dict_pt2[outcome])]
        play = Play(elves, you)
        score = (point_dict[play.you] + point_dict[shape_names_dict_pt2[outcome]])
        res = Result(shape_names_dict_pt2[outcome], score)
    else
        elves, you = split(line, " ")
        play = Play(elves, you)
        outcome = shape_vs_dict[(play.elves, play.you)]
        score = (point_dict[play.you] + point_dict[outcome])
        res = Result(outcome, score)
    end
    play_readable = Play(shape_names_dict[play.elves], shape_names_dict[play.you])
    return Turn(play_readable, res)
end

struct Statistics
    total_turns::Int64
    player_score::Int64
    player_draws::Int64
    player_wins::Int64
    player_losses::Int64
    player_rock::Int64
    player_paper::Int64
    player_scissors::Int64
    elves_draws::Int64
    elves_wins::Int64
    elves_losses::Int64
    elves_rock::Int64
    elves_paper::Int64
    elves_scissors::Int64
end
struct Game
    turns::Array{Turn}
    stats::Statistics
end

function createStatistics(turns::Array{Turn})::Statistics
    total_turns = length(turns)
    player_score = sum(t.result.score for t in turns)
    player_draws = length(filter(t -> (t.result.outcome == "draw"), turns))
    player_wins = length(filter(t -> (t.result.outcome == "win"), turns))
    player_losses = length(filter(t -> (t.result.outcome == "loss"), turns))
    player_rock = length(filter(t -> (t.play.you == "rock"), turns))
    player_paper = length(filter(t -> (t.play.you == "paper"), turns))
    player_scissors = length(filter(t -> (t.play.you == "scissors"), turns))
    elves_draws = player_draws
    elves_wins = player_losses
    elves_losses = player_wins
    elves_rock = length(filter(t -> (t.play.elves == "rock"), turns))
    elves_paper = length(filter(t -> (t.play.elves == "paper"), turns))
    elves_scissors = length(filter(t -> (t.play.elves == "scissors"), turns))
    return Statistics(
        total_turns,
        player_score,
        player_draws,
        player_wins,
        player_losses,
        player_rock,
        player_paper,
        player_scissors,
        elves_draws,
        elves_wins,
        elves_losses,
        elves_rock,
        elves_paper,
        elves_scissors
    )
end


Base.show(io::IO, s::Statistics) = print(io, """
Total Turns: $(s.total_turns)
Player Score: $(s.player_score)
Player Draws: $(s.player_draws)
Player Wins: $(s.player_wins)
Player Losses: $(s.player_losses)
Player Rock: $(s.player_rock)
Player Paper: $(s.player_paper)
Player Scissors: $(s.player_scissors)
Elves Draws: $(s.elves_draws)
Elves Wins: $(s.elves_wins)
Elves Losses: $(s.elves_losses)
Elves Rock: $(s.elves_rock)
Elves Paper: $(s.elves_paper)
Elves Scissors: $(s.elves_scissors)
""")
    

# Part 1 + 2
function with_structs(input, pt2=false)::Game
    turns = [play(line, pt2) for line in input]
    stats = createStatistics(turns)
    return Game(turns, stats)
end

game_1 = @time with_structs(input)
println("Part 1 with structs: $(game_1.stats.player_score)")
println("Part 1 statistics:\n $(game_1.stats)")

game_2 = @time with_structs(input, true)
println("Part 2 with structs: $(game_2.stats.player_score)")
println("Part 2 statistics:\n $(game_2.stats)")

