import { Heart, MessageCircle, Send } from "lucide-react";

export default function PostCard({ post, onLike }) {
  return (
    <article className="panel overflow-hidden p-0">
      <div className="flex items-center gap-3 p-4">
        <span className="grid h-11 w-11 place-items-center rounded-full bg-ink font-black text-white dark:bg-white dark:text-ink">
          {(post.author_detail?.username || post.author_detail?.email || "U")[0].toUpperCase()}
        </span>
        <div>
          <h2 className="font-black">{post.author_detail?.username || post.author_detail?.email || "Creator"}</h2>
          <p className="text-xs font-semibold uppercase tracking-[0.12em] text-slate-500">{post.author_detail?.role || "Member"}</p>
        </div>
      </div>
      <div className="aspect-[4/3] bg-gradient-to-br from-brand via-saffron to-coral">
        {post.external_media_url || post.media ? (
          <img className="h-full w-full object-cover" src={post.external_media_url || post.media} alt="" />
        ) : (
          <div className="flex h-full items-center justify-center p-8 text-center text-3xl font-black text-white">Campaign Story</div>
        )}
      </div>
      <div className="space-y-3 p-4">
        <div className="flex items-center gap-2">
          <button className="btn-secondary h-10 w-10 px-0" onClick={() => onLike?.(post)} aria-label="Like post"><Heart size={17} /></button>
          <button className="btn-secondary h-10 w-10 px-0" aria-label="Comment"><MessageCircle size={17} /></button>
          <button className="btn-secondary h-10 w-10 px-0" aria-label="Share"><Send size={17} /></button>
        </div>
        <p className="text-sm font-bold">{post.like_count || 0} likes</p>
        <p className="text-sm leading-6 text-slate-700 dark:text-slate-300">{post.caption}</p>
        <p className="text-xs text-slate-500">{post.comment_count || 0} comments</p>
      </div>
    </article>
  );
}
