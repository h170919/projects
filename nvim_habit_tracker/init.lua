--- NOTE TEMPLATE START ---
local function insert_script_output()
	local handle = io.popen("bash /Volumes/notes/note_template.sh")
	local script_output = handle:read("*a")
	handle:close()

	local script_lines = {}
	for line in script_output:gmatch("([^\n]*)\n?") do
		table.insert(script_lines, line)
	end

	vim.api.nvim_put(script_lines, "l", true, true)
end
vim.api.nvim_create_user_command("NoteTemplate", insert_script_output, {})
--- NOTE TEMPLATE END ---

--- Update habit streaks START ---
local function insert_streaks_script_output()
	local handle = io.popen("bash /Volumes/notes/streaks.sh")
	local script_output = handle:read("*a")
	handle:close()

	local script_lines = {}
	for line in script_output:gmatch("([^\n]*)\n?") do
		table.insert(script_lines, line)
	end

	vim.api.nvim_put(script_lines, "l", true, true)
end
vim.api.nvim_create_user_command("UpdateStreaks", insert_streaks_script_output, {})

--- UPDATE HABIT STREAKS END ---
