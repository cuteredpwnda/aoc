using Dates
using DotEnv
DotEnv.config(path=joinpath(@__DIR__, "..", ".env"))

baseurl = "https://adventofcode.com/2022/day"
function padDate(date::Int64)
    println("$date, date<10: $(date<10)")
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


if today === nothing
    day_pad = "01"
    baseurl = "https://adventofcode.com/2021/day"
elseif today > 25
    day_pad = "25"
    baseurl = "https://adventofcode.com/2021/day"
end

templates = joinpath(@__DIR__, "templates")
if !isnothing((day_pad))
    folder_template = "day_$day_pad"
    if !isdir(folder_template)
        # make folder
        mkpath(folder_template)
        # Copy template files
        cp("$templates/day_xx.jl", joinpath(folder_template, "day_$day_pad.jl"))
    else
        println("Folder already exists.")
    end
    if !isdir(joinpath(folder_template, "input"))
        # get input
        mkpath(joinpath(folder_template, "input"))
        url = "$baseurl/$day_pad/input"
        cookie = ENV["AOC_COOKIE"]
        # get input
        run(`curl $url --output $folder_template/input/input.txt --cookie "session=$cookie"`)
    end
else
    println("No folder created, day ($day_pad) is not in range")
end