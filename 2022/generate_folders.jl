using Dates
using DotEnv
DotEnv.config(path=joinpath(@__DIR__, "..", ".env"))

baseurl = "https://adventofcode.com/2022/day"
function padDate(date::Int64)
    if date < 10
        return "0$date"
    elseif date > 25
        return nothing
    else
        return "$date"
    end
end

today = Dates.day(now())
day_pad = padDate(today)
test_day = padDate(Dates.day(now() + Day(1)))

if today === nothing
    today = "01"
    baseurl = "https://adventofcode.com/2021/day"
elseif today > 25
    today = "25"
    baseurl = "https://adventofcode.com/2021/day"
end

templates = joinpath(@__DIR__, "templates")
if !isnothing((today))
    folder_template = "day_$today"
    if !isdir(folder_template)
        # make folder
        mkpath(folder_template)
        # Copy template files
        cp("$templates/day_xx.jl", joinpath(folder_template, "day_$today.jl"))
    else
        println("Folder already exists.")
    end
    if !isdir(joinpath(folder_template, "input"))
        # get input
        mkpath(joinpath(folder_template, "input"))
        url = "$baseurl/$today/input"
        cookie = ENV["AOC_COOKIE"]
        # get input
        run(`curl $url --output $folder_template/input/input.txt --cookie "session=$cookie"`)
    end
else
    println("No folder created, day ($today) is not in range")
end