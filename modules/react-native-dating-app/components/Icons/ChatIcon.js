import * as React from "react"
import Svg, { Path } from "react-native-svg"

function ChatIcon(props) {
  return (
    <Svg
      width={16}
      height={16}
      viewBox="0 0 16 16"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      {...props}
    >
      <Path
        d="M16 7.501c0 4.143-3.582 7.501-8 7.501a8.493 8.493 0 01-2.347-.328c-.584.317-1.925.926-4.181 1.322-.2.035-.352-.188-.273-.387.354-.896.674-2.09.77-3.179C.744 11.112 0 9.387 0 7.501 0 3.358 3.582 0 8 0s8 3.358 8 7.501zm-11 0c0-.284-.105-.557-.293-.758A.967.967 0 004 6.43a.967.967 0 00-.707.314A1.112 1.112 0 003 7.501c0 .284.105.557.293.758A.967.967 0 004 8.573c.265 0 .52-.113.707-.314C4.895 8.058 5 7.785 5 7.5zm4 0c0-.284-.105-.557-.293-.758A.967.967 0 008 6.43a.967.967 0 00-.707.314A1.112 1.112 0 007 7.501c0 .284.105.557.293.758A.967.967 0 008 8.573c.265 0 .52-.113.707-.314C8.895 8.058 9 7.785 9 7.5zm3 1.072c.265 0 .52-.113.707-.314.188-.201.293-.474.293-.758 0-.284-.105-.557-.293-.758A.967.967 0 0012 6.43a.967.967 0 00-.707.314 1.112 1.112 0 00-.293.758c0 .284.105.557.293.758a.967.967 0 00.707.314z"
        fill="#000"
      />
    </Svg>
  )
}

export default ChatIcon