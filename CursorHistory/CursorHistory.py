import sublime, sublimeplugin
cursorHistory = []
historyPosition = 0
justNavigated = 0
debug = 0

def debugPrint(text):
	global debug
	if (debug == 1):
		print text

class goBackInCursorHistory(sublimeplugin.TextCommand):
	def run(self, view, args):
		global historyPosition, cursorHistory, justNavigated

		if (historyPosition - 1 < 0):
			debugPrint("at beginning")
			return
					
		justNavigated = 1

		historyPosition = historyPosition - 1
		point = cursorHistory[historyPosition][1]

		view.window().focusView(cursorHistory[historyPosition][0])

		selectionSet = cursorHistory[historyPosition][0].sel()
		selectionSet.clear()

		backRegion = sublime.Region(point, point)
		selectionSet.add(backRegion)

		cursorHistory[historyPosition][0].show(point)

		debugPrint("Going backward to: " + `historyPosition` + " / " + `len(cursorHistory)-1` + " id: " + `cursorHistory[historyPosition][0].bufferId()`)


class goForwardInCursorHistory(sublimeplugin.TextCommand):
	def run(self, view, args):
		global historyPosition, cursorHistory, justNavigated

		if (historyPosition + 1 >= len(cursorHistory)):
			debugPrint("at end")
			return
				
		justNavigated = 1

		historyPosition = historyPosition + 1
		point = cursorHistory[historyPosition][1]

		view.window().focusView(cursorHistory[historyPosition][0])
		selectionSet = cursorHistory[historyPosition][0].sel()
		selectionSet.clear()

		backRegion = sublime.Region(point, point)
		selectionSet.add(backRegion)

		cursorHistory[historyPosition][0].show(point)

		debugPrint("Going forward  to: " + `historyPosition` + " / " + `len(cursorHistory)-1` + " id: " + `cursorHistory[historyPosition][0].bufferId()`)


class PrintCursorHistoryCommand(sublimeplugin.TextCommand):
	def run(self, view, args):
		global cursorHistory
		debugPrint(cursorHistory)

class ClearCursorHistoryCommand(sublimeplugin.TextCommand):
	def run(self, view, args):
		global cursorHistory, historyPosition
		del cursorHistory[:]
		historyPosition = 0

class CursorHistoryCommand(sublimeplugin.Plugin):
	def onSelectionModified(self, view):
		global historyPosition, cursorHistory, justNavigated

		if (justNavigated == 1):
			justNavigated = 0
			return

		point = view.sel()[0].begin()
		line, col = view.rowcol(view.sel()[0].begin())

		if (len(cursorHistory) > 0):
			lastPosition = cursorHistory[-1]

			if (view.id() == lastPosition[0].id()):
				lastRow, lastCol = view.rowcol(lastPosition[1])

				if (lastRow == line):
					debugPrint("on same line")
					return

				if (abs(lastRow - line) < 5):
					debugPrint("too close")
					return

		if (len(cursorHistory) > 0):
			if (historyPosition != len(cursorHistory) - 1):
				debugPrint("Cutting off at " + `historyPosition`)
				cursorHistory = cursorHistory[:(historyPosition)]


		cursorHistory.append((view, point))
		historyPosition = len(cursorHistory) - 1
		debugPrint("Recording cursor: " + `historyPosition` + " / " + `len(cursorHistory)-1` + " id: " + `view.bufferId()`)
