import { ImagePlus, Send } from "lucide-react";
import { useEffect, useState } from "react";

import { feedService } from "../api/services";
import PostCard from "../components/social/PostCard";

export default function FeedPage() {
  const [posts, setPosts] = useState([]);
  const [caption, setCaption] = useState("");
  const [externalMediaUrl, setExternalMediaUrl] = useState("");

  const load = () => feedService.list().then(({ data }) => setPosts(data.results || data)).catch(() => setPosts([]));
  useEffect(() => { load(); }, []);

  const createPost = async (event) => {
    event.preventDefault();
    if (!caption.trim()) return;
    await feedService.create({ caption, external_media_url: externalMediaUrl, hashtags: [] });
    setCaption("");
    setExternalMediaUrl("");
    load();
  };

  const toggleLike = async (post) => {
    await (post.is_liked ? feedService.unlike(post.id) : feedService.like(post.id));
    load();
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[280px_1fr_320px]">
      <aside className="hidden space-y-3 lg:block">
        {["Home feed", "Brand posts", "Creator posts", "Saved campaigns", "Collaboration rooms"].map((item) => (
          <button key={item} className="surface w-full px-4 py-3 text-left text-sm font-black hover:bg-white dark:hover:bg-white/15">{item}</button>
        ))}
      </aside>
      <section className="space-y-5">
        <form className="panel space-y-3" onSubmit={createPost}>
          <p className="eyebrow">Share an update</p>
          <textarea className="input min-h-24" placeholder="Post campaign progress, creator availability, portfolio drops, or brand briefs." value={caption} onChange={(event) => setCaption(event.target.value)} />
          <div className="flex flex-col gap-3 sm:flex-row">
            <input className="input" placeholder="Image or video URL" value={externalMediaUrl} onChange={(event) => setExternalMediaUrl(event.target.value)} />
            <button className="btn-primary shrink-0" type="submit"><Send size={16} /> Publish</button>
          </div>
        </form>
        {posts.length === 0 ? (
          <div className="panel flex min-h-80 flex-col items-center justify-center text-center">
            <ImagePlus className="text-brand" size={42} />
            <h2 className="mt-4 text-2xl font-black">No posts yet</h2>
            <p className="mt-2 max-w-md text-sm leading-6 text-slate-500">Your feed is ready for real brand and creator updates from the API. Create the first post to start the network.</p>
          </div>
        ) : posts.map((post) => <PostCard key={post.id} post={post} onLike={toggleLike} />)}
      </section>
      <aside className="space-y-4">
        <div className="panel">
          <p className="eyebrow">Why this matters</p>
          <h2 className="mt-2 text-lg font-black">No campaign manager required</h2>
          <p className="mt-3 text-sm leading-6 text-slate-500">Brands and creators can discover each other, coordinate content, launch ads, track analytics, and manage conversations directly.</p>
        </div>
      </aside>
    </div>
  );
}
