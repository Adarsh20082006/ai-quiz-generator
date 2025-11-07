export default function Loader({ text = "Generating quiz..." }) {
    return (
        <div className="flex flex-col items-center justify-center p-10 text-center space-y-4">
            <div className="w-12 h-12 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
            <p className="text-slate-600 font-medium">{text}</p>
        </div>
    );
}
