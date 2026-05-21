export default function CardPLSkeleton() {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-5 flex flex-col gap-3 animate-pulse">
      <div className="flex items-start justify-between gap-2">
        <div className="h-3 bg-gray-200 rounded w-32" />
        <div className="h-5 bg-gray-200 rounded-full w-24" />
      </div>
      <div>
        <div className="h-6 bg-gray-200 rounded w-28 mb-2" />
        <div className="h-3 bg-gray-200 rounded w-48" />
      </div>
      <div className="space-y-2 flex-1">
        <div className="h-3 bg-gray-200 rounded w-full" />
        <div className="h-3 bg-gray-200 rounded w-full" />
        <div className="h-3 bg-gray-200 rounded w-3/4" />
      </div>
      <div className="flex items-center justify-between pt-3 border-t border-gray-100">
        <div className="space-y-1.5">
          <div className="h-2.5 bg-gray-200 rounded w-24" />
          <div className="h-2.5 bg-gray-200 rounded w-20" />
        </div>
        <div className="h-4 bg-gray-200 rounded w-24" />
      </div>
    </div>
  );
}