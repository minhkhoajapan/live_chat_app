const ChatMessageKebabMenu = ({isLocalSender, onToggleDropdown, isActive, index, onDeleteMessage}) => {
  return (
    <div className="relative">
      <button
        className={isLocalSender ? "ml-2" : "mr-2"}
        onClick={() => onToggleDropdown(index)}
      >
        <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth="2">
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6v.01M12 12v.01M12 18v.01" />
        </svg>  
      </button>

      {isActive && (
        <div className={`absolute mt-2 w-28 bg-white rounded-md shadow-lg ${isLocalSender ? "left-0" : "right-0"}`}>
          <ul>
            <li 
              className="px-4 py-2 hover:bg-gray-100 cursor-pointer"
              onClick={() => onDeleteMessage(index)}
            >
              Delete
            </li>
          </ul>
        </div>
      )}
    </div>
  )
}

export default ChatMessageKebabMenu;