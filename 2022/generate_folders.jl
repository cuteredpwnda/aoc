using Dates
using DotEnv
DotEnv.config(path=joinpath(@__DIR__, "..", ".env"))

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
tomorrow = today + 1
day_pad = padDate(today)
tomorrow_pad = padDate(tomorrow)

days_to_generate = [day_pad, tomorrow_pad]
for day in days_to_generate
    if day === nothing
        pad = "01"
    elseif parse(Int64, day) > 25
        pad = "25"
        baseurl = "https://adventofcode.com/2021/day"
    else
        pad = day
        baseurl = "https://adventofcode.com/2022/day"
    end


    templates = joinpath(@__DIR__, "templates")
    if !isnothing((pad))
        folder_template = "day_$pad"
        if !isdir(folder_template)
            # make folder
            mkpath(folder_template)
            # Copy template files
            cp("$templates/day_xx.jl", joinpath(folder_template, "day_$pad.jl"))
        else
            println("Folder for day$pad already exists.")
        end
        if parse(Int64, pad) == today
            if !isdir(joinpath(folder_template, "input"))
                mkpath(joinpath(folder_template, "input"))
            end
            url = "$baseurl/$(parse(Int64, pad))/input"
            cookie = ENV["AOC_COOKIE"]
            # get input
            if !isfile(joinpath(folder_template, "input", "input.txt"))
                run(`curl -s $url --output $folder_template/input/input.txt --cookie "session=$cookie"`)
            else
                println("Input already exists.")
            end
        end
    else
        println("No folder created, day ($pad) is not in range")
    end
end