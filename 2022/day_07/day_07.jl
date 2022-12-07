using Parameters

struct File
    filename :: String
    size :: Int64
end
Base.show(io::IO, f::File) = print(
io,"- $(f.filename) (file, size=$(f.size))"
)
@with_kw mutable struct Directory
    dirname :: String
    content :: Union{Array{String}, Nothing} = nothing
    files :: Union{Array{File}, Nothing} = nothing
    parent :: Union{Directory, Nothing} = nothing
    child_dirs :: Union{Array{Directory}, Nothing} = nothing
    files_size :: Union{Int64, Nothing} = nothing
    dir_size :: Union{Int64, Nothing} = nothing
end

Base.:(==)(dir1::Directory, dir2::Directory) = ((dir1.dirname == dir2.dirname) && (dir1.parent == dir2.parent))

function smallprint(dir::Directory) :: String
    return "Dir: $(dir.dirname) fs: $(dir.files_size), ds: $(dir.dir_size), has children: $(dir.child_dirs !== nothing)"
end


Base.show(io::IO, s::Directory) =print(
io,"""\r
Directory: $(s.dirname) (dir) Content: $(s.content === nothing ? "None" : s.content)
Files: $(s.files === nothing ? "None" : [s.filename for s in s.files])
Parent: $(s.parent === nothing ? "None" : s.parent.dirname)
Child Directories: $(s.child_dirs === nothing ? "None" : [x.dirname for x in s.child_dirs])
Files Size: $(s.files_size === nothing ? "None" : s.files_size)
Directory Size: $(s.dir_size === nothing ? "None" : s.dir_size)
"""
)


@with_kw mutable struct Filesystem
    base_dir :: Directory
    directories :: Array{Directory}
end
Base.show(io::IO, fs::Filesystem) = print(
io,"""
Base Directory: $(fs.base_dir.dirname)
Directories: $(fs.directories)
"""
)


function get_subdirs(dir::Directory) :: Array{Directory}
    subdirs = []
    for item in dir.content
        is_dir = match(r"dir ", item)
        if is_dir !== nothing
            dir_name = split(item, " ")[end]
            directory = Directory(dirname=dir_name, parent=dir)
            push!(subdirs, directory)
        end
    end
    return subdirs
end

function get_content(possible_dir_contents::Array) :: Array{String}
    max_index = length(possible_dir_contents)
    for (j, content) in enumerate(possible_dir_contents)
        m = match(r"^\$ ", content)
        # checks if this is the last line of the input
        if j == length(possible_dir_contents) 
            return possible_dir_contents
        end
        # check if new command
        if  m !== nothing
            max_index = j
            break
        end
    end
    return possible_dir_contents[1:max_index-1]
end

function get_dir_file_size(dir::Directory) :: Int64
    if dir.files === nothing
        return 0
    end
    size = 0
    for file in dir.files
        size += file.size
    end
    return size
end

function apply_files_sizes(dir::Directory)
    dir.files_size = get_dir_file_size(dir)
end

# recursive function to get the size of each directory
function apply_dir_sizes(fs::Filesystem, dir::Directory)
    # if directory has child directories, recurse on them
    dir.dir_size = dir.files_size === nothing ? 0 : dir.files_size
    if dir.child_dirs !== nothing
        for child in dir.child_dirs
            subdir = find_dir(fs, child)
            apply_dir_sizes(fs, subdir)
            dir.dir_size += subdir.dir_size
        end        
    elseif dir.child_dirs === nothing
        dir.files_size = get_dir_file_size(dir)
        dir.dir_size = dir.files_size
    end
end

# find directory in filesystem
function find_dir(fs::Filesystem, dir::Directory) :: Union{Directory,Nothing}
    res = fs.directories[findall(x -> x == dir, fs.directories)]
    if res === nothing 
        return nothing
    elseif length(res) == 0
        return error("Directory not found!"), nothing
    elseif length(res) > 1
        println("Multiple directories found: $(res)")
        return error("Multiple directories found!"), nothing
    else 
        return res[1]
    end
end


function update_children(fs::Filesystem, dir::Directory)
    updated_children = []
    if dir.child_dirs !== nothing
        for child in dir.child_dirs
            found = find_dir(fs, child)
            push!(updated_children, found)
        end
        dir.child_dirs = updated_children
    end
end

# Part 1
function part1(input)
    base_dir = Directory(dirname = "\\")
    directories = [base_dir]
    filesystem = Filesystem(base_dir=base_dir, directories = directories)
    parent_dir = nothing
    curr_dir = base_dir
    # get subdirectories and files
    for (i, line) in enumerate(input[2:end])
        ls = match(r"^\$ ls", line)
        cd = match(r"^\$ cd", line)
        sub_dirs = []
        # list contents of directory
        if ls !== nothing
            possible_dir_contents = input[i+2:end]
            curr_dir.content = get_content(possible_dir_contents)
            for item in curr_dir.content
                is_file = match(r"\d+", item)
                is_dir = match(r"dir ", item)
                if is_file !== nothing
                    fn = split(item, " ")[end]
                    file = File(fn, parse(Int64, is_file.match))
                    if curr_dir.files === nothing
                        curr_dir.files = [file]
                    else
                        push!(curr_dir.files, file)
                    end
                end
                if is_dir !== nothing
                    dir_name = split(item, " ")[end]
                    directory = Directory(dirname=dir_name, parent=curr_dir)
                    push!(sub_dirs, directory)
                    curr_dir.child_dirs = sub_dirs
                end
            end
            i += length(curr_dir.content)-1
        end
        # if directory changes
        if cd !== nothing
            dir_name = split(line, " ")[end]
            if dir_name == ".." && parent_dir !== nothing
                curr_dir = parent_dir
                parent_dir = curr_dir.parent
            else
                # go down one level
                parent_dir = curr_dir
                new_dir = Directory(dirname=dir_name, parent=parent_dir)
                curr_dir = new_dir
                push!(directories, new_dir)
            end
        end
    end
    # sort directories by number of child directories
    sort!(filesystem.directories, by = x -> x.child_dirs === nothing ? 0 : length(x.child_dirs))
    for dir in filesystem.directories    
        apply_files_sizes(dir)
        apply_dir_sizes(filesystem, dir)
        update_children(filesystem, dir)
    end
    # filter by size, max is 100000, add them up
    res = filter(x -> x.dir_size <= 100000, filesystem.directories)
    return sum(x -> x.dir_size, res), filesystem
end

# Part 2
function part2(filesystem::Filesystem, input)
    total_space = 70000000
    required_space = 30000000
    currently_used = 0
    for dir in input
        m = match(r"^\d+", dir)
        if m !== nothing
            currently_used += parse(Int64, m.match)
        end
    end
    to_free = required_space - (total_space - currently_used)
    candidates = filter(x -> x.dir_size >= to_free, filesystem.directories)
    # get the smallest dir size
    sort!(candidates, by = x -> x.dir_size)
    return candidates[1].dir_size
end

function main()
    input = open(joinpath(@__DIR__, "input", "input.txt")) do f
        readlines(f)
    end
    p1, fs = part1(input)
    p2 = part2(fs, input)
    @show p1
    @show p2
end

main()