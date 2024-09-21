const LocalSenderChat = ({msg}) => {
  return (
    <>
      <div className="bg-blue-500 text-white rounded-lg p-2 shadow max-w-sm">
        {msg.message && msg.message}
          {msg.file && (
            <img className="max-w-72 min-w-8" src={`http://${baseURL}${msg.file}`} />
          )}
        </div>
    </>
  )
}

export default LocalSenderChat;